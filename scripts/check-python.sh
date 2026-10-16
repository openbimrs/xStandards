#!/usr/bin/env bash
# Build one standard's wheel with maturin, install it into a throwaway uv
# venv, and run its Python suite against it. Used by the gate and CI.
#
#   scripts/check-python.sh openbim-<x>-py
#
# Needs `uv` and `maturin` on PATH (CI pins both; see .github/workflows).
set -euo pipefail

crate="${1:?usage: $0 openbim-<x>-py}"
root="$(cd "$(dirname "$0")/.." && pwd)"
crate_dir="$root/crates/$crate"
[[ "$crate" == openbim-*-py && -f "$crate_dir/pyproject.toml" ]] || {
    echo "error: $crate is not a Python binding crate with pyproject.toml" >&2
    exit 1
}
for tool in uv maturin; do
    command -v "$tool" >/dev/null || { echo "error: $tool not on PATH" >&2; exit 1; }
done

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
uv venv --quiet --python "${PYTHON:-python3}" "$work/venv"

crate_version="$(sed -n 's/^version = "\(.*\)"$/\1/p' "$crate_dir/Cargo.toml" | head -1)"
py_version="$(sed -n 's/^version = "\(.*\)"$/\1/p' "$crate_dir/pyproject.toml" | head -1)"
if [[ "$crate_version" != "$py_version" ]]; then
    echo "error: pyproject.toml version $py_version != Cargo.toml $crate_version" >&2
    exit 1
fi

maturin build --quiet --release --locked --manifest-path "$crate_dir/Cargo.toml" --out "$work/dist"
uv pip install --quiet --python "$work/venv/bin/python" "$work"/dist/*.whl

# Run from outside the source tree so the tests import the installed wheel.
cd "$work"
"$work/venv/bin/python" -m unittest discover \
    -s "$crate_dir/tests/python" -t "$crate_dir/tests/python" -v
