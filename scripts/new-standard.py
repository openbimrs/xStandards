#!/usr/bin/env python3
"""Scaffold the crates of one X-standard.

Every standard in this repository is the same four crates under `crates/`:

    openbim-<slug>        the implementation (crates.io)
    <slug>                short-name alias, a pure re-export (crates.io);
                          skipped with --no-alias when crates.io has the name
    openbim-<slug>-wasm   JavaScript binding, npm `@openbim/<slug>`
    openbim-<slug>-py     Python binding, PyPI `openbim-<slug>`

Usage:
    scripts/new-standard.py xplanung --name XPlanung \\
        --operator "XLeitstelle Planen und Bauen" \\
        --homepage https://xleitstelle.de/xplanung \\
        --summary "Exchange standard for spatial and land-use plans" \\
        --keyword planning

The script refuses to overwrite an existing crate directory. After running
it, add the standard to the table in README.md and AGENTS.md, run
`cargo generate-lockfile` (or any cargo command), and `scripts/gate.sh`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = "https://github.com/openbimrs/xStandards"
VERSION = "0.1.0"
# Pinned exactly: the wasm-bindgen CLI in CI must equal this, and pyo3 is
# pinned so the abi3 wheel stays reproducible. Bump in every binding at once.
WASM_BINDGEN = "0.2.128"
PYO3 = "0.29.2"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def changelog(crate: str) -> str:
    return f"""# Changelog

All notable changes to `{crate}` are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the crate
adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- Initial scaffold.

[Unreleased]: {REPO}/commits/main
"""


def toml_str(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def core(s: argparse.Namespace) -> None:
    crate = f"openbim-{s.slug}"
    ident = crate.replace("-", "_")
    d = ROOT / "crates" / crate
    keywords = ", ".join(toml_str(k) for k in ["openbim", s.slug, "egovernment", *s.keyword][:5])
    write(d / "Cargo.toml", f"""[package]
name = "{crate}"
version = "{VERSION}"
description = {toml_str(f"{s.name} for Rust: {s.summary[0].lower() + s.summary[1:]}")}
edition.workspace = true
rust-version.workspace = true
license.workspace = true
authors.workspace = true
repository.workspace = true
homepage.workspace = true
documentation = "https://docs.rs/{crate}"
readme = "README.md"
keywords = [{keywords}]
categories = ["data-structures", "parser-implementations"]
include = ["src/**", "Cargo.toml", "README.md", "CHANGELOG.md", "LICENSE"]

[dependencies]

[lints]
workspace = true
""")
    homepage = f'Some("{s.homepage}")' if s.homepage else "None"
    homepage_doc = f"\n//! Official information: <{s.homepage}>.\n//!" if s.homepage else "\n//!"
    write(d / "src" / "lib.rs", f"""//! # {crate}
//!
//! {s.summary}.
//! Operated by {s.operator}.{homepage_doc}
//! **Status: scaffold.** This crate currently states only which standard it
//! implements. Reading, writing and validating {s.name} documents are not
//! implemented yet; nothing here encodes normative content of the standard.
//!
//! ```
//! assert_eq!({ident}::NAME, "{s.name}");
//! ```

/// The standard's name as its operator writes it.
pub const NAME: &str = "{s.name}";

/// The body that operates and maintains the standard.
pub const OPERATOR: &str = {toml_str(s.operator)};

/// The operator's public page for the standard, if it has one.
pub const HOMEPAGE: Option<&str> = {homepage};

/// The version of this crate (not of the standard).
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

""")
    write(d / "README.md", f"""# {crate}

{s.summary}, for Rust. {s.name} is operated by {s.operator}.

**Status: scaffold.** The crate states which standard it implements; reading,
writing and validating {s.name} documents are not implemented yet.

```toml
[dependencies]
{crate} = "0.1"
```

Also available as [`@openbim/{s.slug}`](https://www.npmjs.com/package/@openbim/{s.slug})
on npm and [`openbim-{s.slug}`](https://pypi.org/project/openbim-{s.slug}/) on PyPI.

## License

MIT
""")
    write(d / "CHANGELOG.md", changelog(crate))
    write(d / "LICENSE", (ROOT / "LICENSE").read_text(encoding="utf-8"))


def alias(s: argparse.Namespace) -> None:
    crate = s.slug
    canonical = f"openbim-{s.slug}"
    d = ROOT / "crates" / crate
    write(d / "Cargo.toml", f"""[package]
name = "{crate}"
version = "{VERSION}"
description = "{s.name} alias: re-exports {canonical}."
edition.workspace = true
rust-version.workspace = true
license.workspace = true
authors.workspace = true
repository.workspace = true
homepage.workspace = true
documentation = "https://docs.rs/{canonical}"
readme = "README.md"
keywords = ["openbim", "{s.slug}", "egovernment"]
categories = ["data-structures"]
include = ["src/**", "Cargo.toml", "README.md", "CHANGELOG.md", "LICENSE"]

[dependencies]
# Exact pin prevents the alias and canonical package from exposing different
# versions of the same API in one dependency graph.
{canonical} = {{ path = "../{canonical}", version = "={VERSION}" }}

[lints]
workspace = true
""")
    write(d / "src" / "lib.rs", f"""//! Alias for the [`{canonical}`](https://docs.rs/{canonical}) crate.
//!
//! This crate deliberately defines **nothing** of its own. It exists so
//! {s.name} is reachable under the short name practitioners actually use,
//! while there remains exactly one definition of every type.
//!
//! Adding a type here would be a defect: a dependency graph containing both
//! this crate and `{canonical}` would then hold two structurally identical
//! but distinct types, which no Cargo version resolution can unify. The
//! dependency is pinned with `=` for the same reason.
pub use {canonical.replace("-", "_")}::*;
""")
    write(d / "README.md", f"""# {crate}

Short-name package for {s.name}.

This crate is a **pure re-export** of
[`{canonical}`](https://crates.io/crates/{canonical}). It defines nothing of
its own, so both package names expose one canonical API and one type identity.
The dependency is pinned to the exact canonical version.

```toml
{crate} = "0.1"
# equivalent API to:
{canonical} = "0.1"
```

## License

MIT
""")
    write(d / "CHANGELOG.md", changelog(crate))
    write(d / "LICENSE", (ROOT / "LICENSE").read_text(encoding="utf-8"))


def wasm(s: argparse.Namespace) -> None:
    canonical = f"openbim-{s.slug}"
    crate = f"{canonical}-wasm"
    module = crate.replace("-", "_")
    d = ROOT / "crates" / crate
    write(d / "Cargo.toml", f"""[package]
name = "{crate}"
version = "{VERSION}"
description = "WebAssembly bindings for {canonical} ({s.name}), published to npm as @openbim/{s.slug}."
edition.workspace = true
rust-version.workspace = true
license.workspace = true
authors.workspace = true
repository.workspace = true
homepage.workspace = true
keywords = ["openbim", "{s.slug}", "egovernment", "wasm"]
categories = ["wasm"]
# npm-only: distributed as `@openbim/{s.slug}`.
publish = false

[lib]
crate-type = ["cdylib", "rlib"]

[dependencies]
{canonical} = {{ path = "../{canonical}", version = "{VERSION}" }}
wasm-bindgen = "={WASM_BINDGEN}"

[lints]
workspace = true
""")
    write(d / "src" / "lib.rs", f"""//! JavaScript binding of [`{canonical}`], published to npm as
//! `@openbim/{s.slug}`. Build it with `scripts/build-npm-package.sh {crate}`.

use wasm_bindgen::prelude::*;

/// The package version.
#[wasm_bindgen]
#[must_use]
pub fn version() -> String {{
    env!("CARGO_PKG_VERSION").to_owned()
}}

/// The name of the standard this package implements.
#[wasm_bindgen(js_name = standardName)]
#[must_use]
pub fn standard_name() -> String {{
    {canonical.replace("-", "_")}::NAME.to_owned()
}}

#[cfg(test)]
mod tests {{
    #[test]
    fn reports_the_canonical_standard() {{
        assert_eq!(super::standard_name(), {canonical.replace("-", "_")}::NAME);
        assert_eq!(super::version(), env!("CARGO_PKG_VERSION"));
    }}
}}
""")
    package = {
        "name": f"@openbim/{s.slug}",
        "description": f"{s.summary}, in JavaScript (WebAssembly build of {canonical}).",
        "version": VERSION,
        "license": "MIT",
        "repository": {
            "type": "git",
            "url": "git+https://github.com/openbimrs/xStandards.git",
            "directory": f"crates/{crate}",
        },
        "type": "commonjs",
        "main": f"{module}.js",
        "types": f"{module}.d.ts",
        "exports": {
            ".": {
                "node": {"types": f"./{module}.d.ts", "default": f"./{module}.js"},
                "default": {"types": f"./bundler/{module}.d.ts", "default": f"./bundler/{module}.js"},
            },
            "./bundler": {"types": f"./bundler/{module}.d.ts", "default": f"./bundler/{module}.js"},
            "./web": {"types": f"./web/{module}.d.ts", "default": f"./web/{module}.js"},
            "./package.json": "./package.json",
        },
        "files": [
            f"{module}.js", f"{module}.d.ts", f"{module}_bg.wasm", f"{module}_bg.wasm.d.ts",
            "bundler/", "web/", "README.md", "LICENSE",
        ],
        "engines": {"node": ">=18"},
        "keywords": [s.slug, "egovernment", "openbim", "bim", "wasm", *s.keyword],
    }
    write(d / "npm" / "package.json", json.dumps(package, indent=2, ensure_ascii=False) + "\n")
    write(d / "tests" / "js" / "smoke.cjs", f"""// Runs against the built package: XSTD_NPM_PKG=<out dir> node --test ...
const assert = require("node:assert/strict");
const path = require("node:path");
const test = require("node:test");

const dir = process.env.XSTD_NPM_PKG;
if (!dir) throw new Error("set XSTD_NPM_PKG to the built package directory");
const pkg = require(path.resolve(dir));
const manifest = require(path.resolve(dir, "package.json"));

test("version matches the package manifest", () => {{
  assert.equal(pkg.version(), manifest.version);
}});

test("names the standard", () => {{
  assert.equal(pkg.standardName(), {json.dumps(s.name)});
}});
""")
    write(d / "README.md", f"""# @openbim/{s.slug}

{s.summary}, in JavaScript: the WebAssembly build of the
[`{canonical}`](https://crates.io/crates/{canonical}) Rust crate.

**Status: scaffold.** The package states which standard it implements;
reading, writing and validating {s.name} documents are not implemented yet.

```js
const {{ standardName, version }} = require("@openbim/{s.slug}");
console.log(standardName(), version());
```

Node uses the CommonJS build; bundlers get `@openbim/{s.slug}/bundler` and
browsers without a bundler `@openbim/{s.slug}/web` (call its default `init()`
first).

## License

MIT
""")
    write(d / "CHANGELOG.md", changelog(crate))
    write(d / "LICENSE", (ROOT / "LICENSE").read_text(encoding="utf-8"))


def python(s: argparse.Namespace) -> None:
    canonical = f"openbim-{s.slug}"
    crate = f"{canonical}-py"
    module = canonical.replace("-", "_")
    d = ROOT / "crates" / crate
    write(d / "Cargo.toml", f"""[package]
name = "{crate}"
version = "{VERSION}"
description = "Python bindings for {canonical} ({s.name}), published to PyPI as openbim-{s.slug}."
edition.workspace = true
rust-version.workspace = true
license.workspace = true
authors.workspace = true
repository.workspace = true
homepage.workspace = true
keywords = ["openbim", "{s.slug}", "egovernment", "python"]
categories = ["api-bindings"]
# Shipped as a wheel (maturin), not as a crate.
publish = false

[lib]
# Python imports the extension as `{module}`; `rlib` lets the Rust tests link
# the binding without an interpreter.
name = "{module}_py"
crate-type = ["cdylib", "rlib"]

[dependencies]
{canonical} = {{ path = "../{canonical}", version = "{VERSION}" }}
# abi3-py39: one wheel for CPython 3.9+. maturin sets
# PYO3_BUILD_EXTENSION_MODULE, so `cargo test --workspace` stays linkable.
pyo3 = {{ version = "={PYO3}", features = ["abi3-py39"] }}

[lints]
workspace = true
""")
    write(d / "src" / "lib.rs", f"""//! Python binding of [`{canonical}`], published to PyPI as
//! `openbim-{s.slug}` and imported as `{module}`. Build and test it with
//! `scripts/check-python.sh {crate}`.

use pyo3::prelude::*;

/// The `{module}` extension module.
#[pymodule]
#[pyo3(name = "{module}")]
fn init(m: &Bound<'_, PyModule>) -> PyResult<()> {{
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add("STANDARD_NAME", ::{module}::NAME)?;
    m.add("OPERATOR", ::{module}::OPERATOR)?;
    m.add("HOMEPAGE", ::{module}::HOMEPAGE)?;
    Ok(())
}}
""")
    write(d / "pyproject.toml", f"""[build-system]
requires = ["maturin>=1.13,<2"]
build-backend = "maturin"

[project]
name = "openbim-{s.slug}"
version = "{VERSION}"
description = {toml_str(f"{s.summary} -- Python bindings for the {canonical} Rust crate.")}
readme = "README.md"
license = {{ text = "MIT" }}
requires-python = ">=3.9"
keywords = [{", ".join(toml_str(k) for k in [s.slug, "egovernment", "openbim", "bim", *s.keyword])}]
classifiers = [
    "Programming Language :: Rust",
    "Programming Language :: Python :: Implementation :: CPython",
    "License :: OSI Approved :: MIT License",
]

[project.urls]
Repository = "{REPO}"

[tool.maturin]
module-name = "{module}"
# maturin moves pyproject.toml to the sdist root but leaves LICENSE in the
# crate directory, while PKG-INFO names it at the root; PyPI rejects such
# an sdist.
include = [{{ path = "LICENSE", format = "sdist" }}]
""")
    write(d / "tests" / "python" / "test_smoke.py", f"""import unittest

import {module}


class Smoke(unittest.TestCase):
    def test_names_the_standard(self):
        self.assertEqual({module}.STANDARD_NAME, {json.dumps(s.name)})

    def test_reports_a_version(self):
        self.assertRegex({module}.__version__, r"^\\d+\\.\\d+\\.\\d+")


if __name__ == "__main__":
    unittest.main()
""")
    write(d / "README.md", f"""# openbim-{s.slug}

{s.summary}, in Python: bindings for the
[`{canonical}`](https://crates.io/crates/{canonical}) Rust crate.

**Status: scaffold.** The package states which standard it implements;
reading, writing and validating {s.name} documents are not implemented yet.

```python
import {module}
print({module}.STANDARD_NAME, {module}.__version__)
```

## License

MIT
""")
    write(d / "CHANGELOG.md", changelog(crate))
    write(d / "LICENSE", (ROOT / "LICENSE").read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slug", help="lowercase crate stem, e.g. xplanung")
    parser.add_argument("--name", required=True, help="official spelling, e.g. XPlanung")
    parser.add_argument("--operator", required=True)
    parser.add_argument("--homepage")
    parser.add_argument("--summary", required=True,
        help="one sentence without a final period, starting with a capital")
    parser.add_argument("--keyword", action="append", default=[])
    parser.add_argument("--no-alias", action="store_true",
        help="skip the short-name alias (its crates.io name is taken)")
    s = parser.parse_args()
    if not re.fullmatch(r"x[a-z0-9-]+", s.slug):
        print(f"slug must be lowercase and start with x: {s.slug}", file=sys.stderr)
        return 1
    dirs = [f"openbim-{s.slug}", f"openbim-{s.slug}-wasm", f"openbim-{s.slug}-py"]
    if not s.no_alias:
        dirs.append(s.slug)
    taken = [d for d in dirs if (ROOT / "crates" / d).exists()]
    if taken:
        print(f"refusing to overwrite: {', '.join(taken)}", file=sys.stderr)
        return 1
    core(s)
    if not s.no_alias:
        alias(s)
    wasm(s)
    python(s)
    print("created " + ", ".join(f"crates/{d}" for d in dirs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
