#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"
PYTHONPATH=src exec python -m unittest discover -s tests -v
