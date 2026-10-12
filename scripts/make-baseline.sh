#!/usr/bin/env bash

set -euo pipefail
mkdir -p waivers
ruff check . --config enforce/python/pyproject.toml --output-format=json > waivers/baseline.ruff.json || true
echo "baseline written to waivers/baseline.ruff.json"
