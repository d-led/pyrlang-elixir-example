#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

if [ -d .venv ]; then
    echo "activating .venv"
    . .venv/bin/activate
fi

echo "starting epmd"
epmd &

echo "running the demo"
python3 example.py
