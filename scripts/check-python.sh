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

# The PyPI short-name alias, if the standard has one: it must pin this
# wheel exactly and expose the same module.
stem="${crate#openbim-}"
stem="${stem%-py}"
alias_dir="$root/crates/$stem/python"
if [[ -f "$alias_dir/pyproject.toml" ]]; then
    alias_version="$(sed -n 's/^version = "\(.*\)"$/\1/p' "$alias_dir/pyproject.toml" | head -1)"
    grep -qx "dependencies = \[\"openbim-$stem==$py_version\"\]" "$alias_dir/pyproject.toml" \
        && [[ "$alias_version" == "$py_version" ]] || {
        echo "error: $stem must be version $py_version and depend on exactly openbim-$stem==$py_version" >&2
        exit 1
    }
    uv build --quiet --wheel --sdist --out-dir "$work/alias" "$alias_dir"
    uv pip install --quiet --python "$work/venv/bin/python" "$work"/alias/*.whl
    "$work/venv/bin/python" -c "
import $stem, openbim_$stem
assert $stem.STANDARD_NAME == openbim_$stem.STANDARD_NAME
assert $stem.__version__ == openbim_$stem.__version__
print('$stem -> openbim_$stem:', $stem.STANDARD_NAME, $stem.__version__)"
fi
