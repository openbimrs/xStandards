#!/usr/bin/env bash
# The complete verification gate, locally and in CI.
#
#   scripts/gate.sh            every section
#   scripts/gate.sh rust       formatting, build, tests, lints, docs, packaging
#   scripts/gate.sh bindings   every npm package and wheel, built and tested
#
# CI runs the sections as parallel jobs; together they are the whole gate.
# `bindings` needs wasm-bindgen-cli (the version pinned in the wasm crates),
# node, uv and maturin.
set -euo pipefail

cd "$(dirname "$0")/.."
if [[ -z "${CARGO_TARGET_DIR:-}" && -d /mnt/backup/build-cache ]]; then
  export CARGO_TARGET_DIR="/mnt/backup/build-cache/openbim-xstandards-target"
fi
target_dir="${CARGO_TARGET_DIR:-target}"

step() { printf '\n==> %s\n' "$*"; "$@"; }

members() {
  # Workspace crates as "<name> <publish>" lines, publish = true|false.
  cargo metadata --format-version 1 --no-deps --locked | python3 -c '
import json, sys
for p in json.load(sys.stdin)["packages"]:
    print(p["name"], "false" if p.get("publish") == [] else "true")'
}

# Standard material (XSD, GML/XML samples, code lists, specification PDFs)
# has no redistribution rights established here. It belongs in the ignored
# references/ directory and must never be tracked or packaged.
standards_payload='\.(xsd|gml|xmi|qea|eap|pdf|zip|sch)$'

structure() {
  # Every standard ships the same crates, and each binding's registry
  # manifest carries the crate version, so one tag is one release.
  python3 - <<'PY'
import json, re, sys, tomllib
from pathlib import Path
crates = Path("crates")
cores = sorted(d.name for d in crates.iterdir() if re.fullmatch(r"openbim-x[a-z0-9]+", d.name))
if len(cores) < 7:
    sys.exit(f"expected at least 7 standards, found {cores}")
errors = []
for core in cores:
    stem = core.removeprefix("openbim-")
    for suffix, manifest, field in (("-wasm", "npm/package.json", "version"),
                                    ("-py", "pyproject.toml", "version")):
        d = crates / f"{core}{suffix}"
        if not d.is_dir():
            errors.append(f"{core}: missing {d.name}")
            continue
        version = tomllib.loads((d / "Cargo.toml").read_text())["package"]["version"]
        text = (d / manifest).read_text()
        declared = json.loads(text)["version"] if manifest.endswith(".json") \
            else tomllib.loads(text)["project"]["version"]
        if declared != version:
            errors.append(f"{d.name}: {manifest} says {declared}, Cargo.toml {version}")
    alias = crates / stem
    if alias.is_dir():
        lib = (alias / "src/lib.rs").read_text()
        code = [l for l in lib.splitlines() if l.strip() and not l.lstrip().startswith("//")]
        if code != [f"pub use {core.replace('-', '_')}::*;"]:
            errors.append(f"{stem}: an alias must only re-export {core}")
        version = tomllib.loads((crates / core / "Cargo.toml").read_text())["package"]["version"]
        req = tomllib.loads((alias / "Cargo.toml").read_text())["dependencies"][core]["version"]
        if req != f"={version}":
            errors.append(f"{stem}: pins {core} {req}, expected ={version}")
for e in errors:
    print(f"gate: {e}", file=sys.stderr)
if errors:
    sys.exit(1)
print(f"{len(cores)} standards: {', '.join(c.removeprefix('openbim-') for c in cores)}")
PY
}

pinned_canonical() {
  sed -n "s/^openbim-$1 = .*version = \"=\([^\"]*\)\".*/\1/p" "crates/$1/Cargo.toml"
}

canonical_live() {
  # The sparse index lists every published version of openbim-<alias>.
  local crate="openbim-$1" version
  version="$(pinned_canonical "$1")"
  curl -fsS "https://index.crates.io/${crate:0:2}/${crate:2:2}/$crate" 2>/dev/null \
    | grep -q "\"vers\":\"$version\""
}

package_crates() {
  # An alias resolves its canonical crate from crates.io when packaged
  # (cargo 1.88 has no workspace-local packaging), so it packages only once
  # the exact canonical version it pins is live; until then the gate says
  # so. Release order is the same: canonical crate first, then the alias.
  local publishable=() name publish
  while read -r name publish; do
    [[ "$publish" == true ]] || continue
    if [[ "$name" != openbim-* ]] && ! canonical_live "$name"; then
      echo "gate: skipping package of $name until openbim-$name $(pinned_canonical "$name") is on crates.io"
      continue
    fi
    publishable+=(-p "$name")
  done < <(members)
  step cargo package "${publishable[@]}" --allow-dirty --locked
  local listing
  listing="$(cargo package "${publishable[@]}" --allow-dirty --locked --list)"
  if printf '%s\n' "$listing" | grep -Ei "$standards_payload|^references/"; then
    echo "gate: standards payload in a crate package (see above)" >&2
    exit 1
  fi
  # Every packaged crate ships its README and LICENSE.
  local i version
  for ((i = 1; i < ${#publishable[@]}; i += 2)); do
    name="${publishable[$i]}"
    version="$(sed -n 's/^version = "\(.*\)"$/\1/p' "crates/$name/Cargo.toml" | head -1)"
    for file in README.md LICENSE; do
      test -f "$target_dir/package/$name-$version/$file" || {
        echo "gate: $name $version does not package $file" >&2
        exit 1
      }
    done
  done
}

section_rust() {
  step structure
  step cargo fmt --all -- --check
  step cargo build --workspace --all-targets --locked
  step cargo test --workspace --all-targets --locked
  step cargo test --workspace --doc --locked
  step cargo clippy --workspace --all-targets --locked -- -D warnings
  RUSTDOCFLAGS="-D warnings" step cargo doc --workspace --no-deps --locked
  for script in scripts/*.py; do step python3 -m py_compile "$script"; done
  if git rev-parse --verify HEAD >/dev/null 2>&1 \
    && git ls-files | grep -Ei "$standards_payload"; then
    echo "gate: standards payload tracked in Git (see above)" >&2
    exit 1
  fi
  package_crates
}

section_bindings() {
  step cargo clippy --target wasm32-unknown-unknown --locked \
    $(members | awk '/-wasm /{print "-p", $1}') -- -D warnings
  while read -r name _; do
    case "$name" in
      openbim-*-wasm)
        step scripts/build-npm-package.sh "$name" "$target_dir/npm/$name"
        stem="${name#openbim-}"; stem="${stem%-wasm}"
        if [[ -f "crates/$stem/npm/package.json" ]]; then
          step scripts/build-npm-alias.sh "$stem" "$target_dir/npm/$stem" "$target_dir/npm/$name"
        fi ;;
      openbim-*-py) step scripts/check-python.sh "$name" ;;
    esac
  done < <(members)
}

case "${1:-all}" in
  rust) section_rust ;;
  bindings) section_bindings ;;
  all) section_rust; section_bindings ;;
  *) echo "usage: $0 [rust|bindings]" >&2; exit 2 ;;
esac

echo
echo "gate: PASS (${1:-all})"
