#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/.github/workflows" "$tmp/waivers" "$tmp/scripts"
cp "$ROOT/.editorconfig" "$ROOT/.pre-commit-config.yaml" "$ROOT/.oxfmtrc.json" "$ROOT/.oxlintrc.json" "$ROOT/VERSION" "$ROOT/CHANGELOG.md" "$tmp/"
cp -r "$ROOT/enforce" "$ROOT/checks" "$tmp/"
cp "$ROOT/.github/workflows/quality.yml" "$tmp/.github/workflows/"
cp "$ROOT/scripts/check_waivers.py" "$ROOT/scripts/check_tree.py" "$tmp/scripts/"
cd "$tmp"
git init -q
git add -A
pre-commit run --all-files
python3 scripts/check_tree.py
python3 scripts/check_waivers.py
echo "starter ok"
