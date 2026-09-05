#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"
PYTHON="${PYTHON:-python}"

PYTHON="$PYTHON" "$SCRIPT_DIR/check.sh"

echo "Building documentation with warnings as errors..."
PYTHON="$PYTHON" "$SCRIPT_DIR/generate_docs.sh"

echo "All complete quality checks passed."
