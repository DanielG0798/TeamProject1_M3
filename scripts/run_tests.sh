#!/usr/bin/env bash
# Run the Milestone 3 ten-case evaluation and write evaluation_results.csv.
set -euo pipefail

cd "$(dirname "$0")/.."

if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run as a module so the repo root is on sys.path (evaluate_m3 imports src.m3_agent).
python -m scripts.evaluate_m3 "$@"
