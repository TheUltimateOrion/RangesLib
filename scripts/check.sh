#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"
PYTHON="${PYTHON:-python}"

echo "Checking Ruff lint rules..."
"$PYTHON" -m ruff check .

echo "Checking Ruff formatting..."
"$PYTHON" -m ruff format --check .

PYTHON="$PYTHON" "$SCRIPT_DIR/typecheck.sh"

echo "Running tests with branch coverage..."
"$PYTHON" -m coverage erase
PYTHONPATH=src "$PYTHON" -m coverage run -m unittest discover -s tests
"$PYTHON" -m coverage report

echo "All local quality checks passed."
