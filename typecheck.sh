#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"
PYTHON="${PYTHON:-python}"

echo "Checking static types with mypy..."
"$PYTHON" -m mypy src/rangeslib tests/typecheck/public_api.py

echo "Checking static types with Pyright..."
"$PYTHON" -m pyright

echo "Static type checks passed."
