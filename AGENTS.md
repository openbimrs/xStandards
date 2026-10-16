# xStandards repository instructions

Canonical `openbimrs/xStandards` repository for the German X-standards
(XÖV and related public-sector exchange standards). One standard, four
crates; see README.md for the table of standards and package names.

## Map

- `crates/openbim-<x>/` — the implementation of standard `<x>` (crates.io)
- `crates/<x>/` — short-name alias, a pure `pub use openbim_<x>::*;` pinned
  with `=` (crates.io); its `npm/` (npm `<x>`, re-exports `@openbim/<x>`)
  and `python/` (PyPI `<x>`, re-exports `openbim_<x>`) are the same alias on
  the other registries, released by tags `<x>-npm-v…` and `<x>-py-v…`;
  `xrechnung` has none, the name is taken everywhere
- `crates/openbim-<x>-wasm/` — JavaScript binding, npm `@openbim/<x>`
  (`npm/package.json`, `tests/js/`); `publish = false` on crates.io
- `crates/openbim-<x>-py/` — Python binding, PyPI `openbim-<x>`, imported as
  `openbim_<x>` (`pyproject.toml`, `tests/python/`); `publish = false`
- `scripts/gate.sh` — the complete gate; sections `rust` and `bindings`
- `scripts/new-standard.py` — scaffold the four crates of another standard
- `scripts/release-crate.py`, `.github/workflows/release.yml` — per-crate
  releases (`<crate>-v<version>` tags) to crates.io, npm and PyPI by trusted
  publishing; see CONTRIBUTING.md
- `scripts/build-npm-package.sh`, `scripts/build-npm-alias.sh`,
  `scripts/check-python.sh` — build and test one binding and its alias
- `references/` — ignored; local schema, sample and specification material

## Boundaries

- May depend only on `openbim-core`, `openbim-step`, and IFC crates (see the
  parent `packages/AGENTS.md`); currently it depends on nothing. A standard
  may depend on another standard here when the standard itself builds on it
  (XTrasse on XPlanung, XBreitband on XBau).
- Bindings reach a standard only through its `openbim-<x>` crate. The alias
  crates define nothing; the gate enforces that.
- Never commit, package, or paste schema files (XSD, Schematron), GML/XML
  samples, code lists, or specification text. Redistribution rights are
  established per standard, not assumed. Keep local copies in `references/`.
- Every encoded fact (version, namespace, code list value) must be traceable
  to a public page of the standard's operator; cite it in rustdoc. Do not
  invent normative content. A capability is implemented only with executable
  evidence here.

Run `scripts/gate.sh` before committing. Trust command exit codes.
