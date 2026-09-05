#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"
PYTHON="${PYTHON:-python}"

PYTHON="$PYTHON" ./check.sh

echo "Building documentation with warnings as errors..."
PYTHON="$PYTHON" ./generate_docs.sh

echo "All complete quality checks passed."
