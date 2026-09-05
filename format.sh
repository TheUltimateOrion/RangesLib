#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"
PYTHON="${PYTHON:-python}"

echo "Fixing Ruff lint issues..."
"$PYTHON" -m ruff check . --fix

echo "Formatting Python files with Ruff..."
"$PYTHON" -m ruff format .

echo "Formatting complete. Run ./check.sh before committing."
