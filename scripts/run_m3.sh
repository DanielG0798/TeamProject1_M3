#!/usr/bin/env bash
# Run the Milestone 3 agent with a question supplied by the user.
set -euo pipefail

cd "$(dirname "$0")/.."

if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

if [ "$#" -eq 0 ]; then
    python -m src.m3_agent --interactive
else
    python -m src.m3_agent "$@"
fi
