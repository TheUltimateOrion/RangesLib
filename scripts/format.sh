#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"
PYTHON="${PYTHON:-python}"

echo "Fixing Ruff lint issues..."
"$PYTHON" -m ruff check . --fix

echo "Formatting Python files with Ruff..."
"$PYTHON" -m ruff format .

echo "Formatting complete. Run ./scripts/check.sh before committing."
