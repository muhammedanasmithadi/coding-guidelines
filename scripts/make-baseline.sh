#!/usr/bin/env bash
set -euo pipefail
# Writes current violations to waivers/baseline.<tool>.json for ratchet mode.
# Usage: scripts/make-baseline.sh
mkdir -p waivers
ruff check . --output-format=json > waivers/baseline.ruff.json || true
echo "baseline written to waivers/baseline.ruff.json"
