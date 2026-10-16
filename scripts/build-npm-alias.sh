#!/usr/bin/env bash
# Assemble the npm short-name alias `<x>` (crates/<x>/npm) and check that it
# re-exports @openbim/<x> exactly.
#
#   scripts/build-npm-alias.sh <x> <out-dir> [canonical-package-dir]
#
# With a canonical package directory (the gate passes the one
# build-npm-package.sh just built) the alias is tested against it; without
# one (a release) the pinned @openbim/<x> is installed from npm, so the
# canonical package must be published first.
set -euo pipefail

stem="${1:?usage: $0 <x> <out-dir> [canonical-package-dir]}"
out="${2:?usage: $0 <x> <out-dir> [canonical-package-dir]}"
canonical="${3:-}"
root="$(cd "$(dirname "$0")/.." && pwd)"
src="$root/crates/$stem/npm"
[[ -f "$src/package.json" ]] || { echo "error: $src/package.json missing" >&2; exit 1; }

python3 - "$src/package.json" "$root/crates/openbim-$stem-wasm/npm/package.json" <<'PY'
import json, sys
alias, binding = (json.load(open(p)) for p in sys.argv[1:])
want = {binding["name"]: binding["version"]}
if alias["dependencies"] != want or alias["version"] != binding["version"]:
    sys.exit(f"{alias['name']} must be version {binding['version']} and depend on exactly {want}")
PY

rm -rf "$out"
mkdir -p "$out"
cp -r "$src"/. "$out"/

test_dir="$(mktemp -d)"
trap 'rm -rf "$test_dir"' EXIT
mkdir -p "$test_dir/node_modules/@openbim"
cp -r "$out" "$test_dir/node_modules/$stem"
if [[ -n "$canonical" ]]; then
    cp -r "$canonical" "$test_dir/node_modules/@openbim/$stem"
else
    version="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$src/package.json")"
    (cd "$test_dir" && npm install --no-save --no-audit --no-fund --loglevel=error "@openbim/$stem@$version")
fi
(cd "$test_dir" && node -e '
const assert = require("node:assert/strict");
const [alias, canonical] = [process.argv[1], "@openbim/" + process.argv[1]];
assert.equal(require(alias), require(canonical), "alias must re-export the canonical module");
console.log(`${alias} -> ${canonical}: ${require(alias).standardName()} ${require(alias).version()}`);
' "$stem")
(cd "$out" && npm pack --dry-run >/dev/null 2>&1)
