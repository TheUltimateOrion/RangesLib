#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"
PYTHON="${PYTHON:-python}"
rm -rf docs/_build
PYTHONPATH=src exec "$PYTHON" -m sphinx -W --keep-going -b html docs docs/_build/html
