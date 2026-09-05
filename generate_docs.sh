#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"
PYTHON="${PYTHON:-python}"
rm -rf docs/_build
PYTHONPATH=src exec "$PYTHON" -m sphinx -W --keep-going -b html docs docs/_build/html
