#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"
rm -rf docs/_build
PYTHONPATH=src exec .venv/bin/sphinx-build -b html docs docs/_build/html
