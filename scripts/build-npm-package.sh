#!/usr/bin/env bash
# Build one standard's npm package from its wasm crate, then test it.
#
#   scripts/build-npm-package.sh openbim-<x>-wasm [out-dir]
#
# One release build of the wasm module, bound three times by wasm-bindgen,
# as openbimrs/ifcx's @openbim/ifcx does:
#
#   <out>/            --target nodejs   CommonJS for Node (the `node` condition)
#   <out>/bundler/    --target bundler  ES module for webpack, Rollup (the default)
#   <out>/web/        --target web      ES module with `init()`, no bundler needed
#
# The wasm-bindgen CLI must equal the `wasm-bindgen` crate pin exactly: a
# mismatch fails at bindgen time or generates glue for a different ABI.
set -euo pipefail

crate="${1:?usage: $0 openbim-<x>-wasm [out-dir]}"
root="$(cd "$(dirname "$0")/.." && pwd)"
crate_dir="$root/crates/$crate"
out="${2:-$crate_dir/pkg}"
module="${crate//-/_}"

[[ "$crate" == openbim-*-wasm && -f "$crate_dir/npm/package.json" ]] || {
    echo "error: $crate is not a wasm binding crate with npm/package.json" >&2
    exit 1
}

pinned="$(sed -n 's/^wasm-bindgen = "=\(.*\)"$/\1/p' "$crate_dir/Cargo.toml")"
if [[ -z "$pinned" ]]; then
    echo "error: wasm-bindgen is not pinned with = in $crate_dir/Cargo.toml" >&2
    exit 1
fi
if ! command -v wasm-bindgen >/dev/null; then
    echo "error: wasm-bindgen CLI missing; run: cargo install wasm-bindgen-cli --version $pinned --locked" >&2
    exit 1
fi
installed="$(wasm-bindgen --version | awk '{print $2}')"
if [[ "$installed" != "$pinned" ]]; then
    echo "error: wasm-bindgen CLI $installed != crate $pinned; run: cargo install wasm-bindgen-cli --version $pinned --locked --force" >&2
    exit 1
fi
crate_version="$(sed -n 's/^version = "\(.*\)"$/\1/p' "$crate_dir/Cargo.toml" | head -1)"
npm_version="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$crate_dir/npm/package.json")"
if [[ "$crate_version" != "$npm_version" ]]; then
    echo "error: npm/package.json version $npm_version != Cargo.toml $crate_version" >&2
    exit 1
fi

target_dir="${CARGO_TARGET_DIR:-$root/target}"
(cd "$root" && cargo build -p "$crate" --target wasm32-unknown-unknown --release --locked)
wasm="$target_dir/wasm32-unknown-unknown/release/$module.wasm"

rm -rf "$out"
wasm-bindgen --target nodejs --out-dir "$out" "$wasm"
wasm-bindgen --target bundler --out-dir "$out/bundler" "$wasm"
wasm-bindgen --target web --out-dir "$out/web" "$wasm"

# The nodejs glue is CommonJS. Without its own package.json, Node resolves
# the nearest enclosing one, which may say "type": "module". The two ES
# module targets declare themselves.
cp "$crate_dir/npm/package.json" "$crate_dir/README.md" "$crate_dir/LICENSE" "$out/"
for dir in bundler web; do
    printf '{\n  "type": "module"\n}\n' >"$out/$dir/package.json"
done

XSTD_NPM_PKG="$out" node --test "$crate_dir"/tests/js/*.cjs

# The tarball npm would publish must hold every file package.json promises.
listing="$(mktemp)"
trap 'rm -f "$listing"' EXIT
(cd "$out" && npm pack --dry-run --json >"$listing")
python3 - "$listing" "$out/package.json" <<'PY'
import json, sys
packed = {f["path"] for f in json.load(open(sys.argv[1]))[0]["files"]}
manifest = json.load(open(sys.argv[2]))
missing = [f for f in manifest["files"] if not f.endswith("/") and f not in packed]
missing += [d for d in manifest["files"] if d.endswith("/") and not any(p.startswith(d) for p in packed)]
if missing:
    sys.exit(f"npm package lacks {missing}")
print(f"{manifest['name']}@{manifest['version']}: {len(packed)} files")
PY
