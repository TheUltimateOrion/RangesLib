#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"
PYTHON="${PYTHON:-python}"
PYTHONPATH=src exec "$PYTHON" playground.py
