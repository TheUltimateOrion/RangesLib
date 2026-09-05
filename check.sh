#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"
PYTHON="${PYTHON:-python}"

echo "Checking Ruff lint rules..."
"$PYTHON" -m ruff check .

echo "Checking Ruff formatting..."
"$PYTHON" -m ruff format --check .

PYTHON="$PYTHON" ./typecheck.sh

echo "Running tests with branch coverage..."
"$PYTHON" -m coverage erase
PYTHONPATH=src "$PYTHON" -m coverage run -m unittest discover -s tests
"$PYTHON" -m coverage report

echo "All local quality checks passed."
