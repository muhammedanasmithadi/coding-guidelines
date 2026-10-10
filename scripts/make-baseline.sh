#!/usr/bin/env bash

set -euo pipefail
mkdir -p waivers
ruff check . --output-format=json > waivers/baseline.ruff.json || true
echo "baseline written to waivers/baseline.ruff.json"
