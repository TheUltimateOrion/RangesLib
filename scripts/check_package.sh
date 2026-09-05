#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"
PYTHON="${PYTHON:-python}"

echo "Building source and wheel distributions..."
rm -rf build dist
"$PYTHON" -m build

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

VENV="$TMP_DIR/venv"
"$PYTHON" -m venv "$VENV"
VENV_PYTHON="$VENV/bin/python"

echo "Installing the built wheel into an isolated smoke-test environment..."
"$VENV_PYTHON" -m pip install --disable-pip-version-check dist/*.whl

echo "Smoke-testing the installed wheel outside the source checkout..."
(
    cd "$TMP_DIR"
    "$VENV_PYTHON" - <<'PY'
from importlib.resources import files

from rangeslib import Range, ranges, views

assert list(Range(1, 2, 3)[1:]) == [2, 3]
assert list(ranges.iota(1, 5) | views.take(2)) == [1, 2]
assert files("rangeslib").joinpath("py.typed").is_file()
PY
)

echo "Package build and installed-wheel smoke test passed."
