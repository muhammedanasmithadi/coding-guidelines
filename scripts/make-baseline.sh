#!/usr/bin/env bash

set -euo pipefail
mkdir -p waivers
ruff check . --config enforce/python/pyproject.toml --output-format=json > waivers/baseline.ruff.json || true
echo "baseline written to waivers/baseline.ruff.json"
tmp="waivers/.baseline.check-tree.json.tmp"
python3 scripts/check_tree.py --format=json > "$tmp" || true
mv "$tmp" waivers/baseline.check-tree.json
echo "baseline written to waivers/baseline.check-tree.json"
