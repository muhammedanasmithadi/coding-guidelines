#!/usr/bin/env bash

set -euo pipefail
npm_v() { npm view "$1" version 2>/dev/null || echo unknown; }
pypi_v() { python3 -c "import json,urllib.request; print(json.load(urllib.request.urlopen('https://pypi.org/pypi/$1/json', timeout=15))['info']['version'])" 2>/dev/null || echo unknown; }
echo "== npm =="
for p in prettier eslint typescript typescript-eslint cspell @commitlint/cli; do
  echo "$p latest: $(npm_v "$p")"
done
echo "== pypi =="
for p in ruff black mypy pytest coverage radon pip-audit semgrep lizard pyyaml; do
  echo "$p latest: $(pypi_v "$p")"
done
echo "Compare against package.json, requirements-ci.txt, .python-version, .nvmrc; bump per docs/tooling.md."
