#!/usr/bin/env bash
# Run the Milestone 3 agent with example inputs.
set -euo pipefail

cd "$(dirname "$0")/.."

if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

python -m src.m3_agent \
    --course physics_101 \
    --question "I am stuck setting up Newton's second law."
