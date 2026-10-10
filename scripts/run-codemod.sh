#!/usr/bin/env bash

set -euo pipefail
SG="${1:-}"
PATH_="${2:-.}"
if [ -z "$SG" ]; then echo "usage: run-codemod.sh <sgconfig.yml> [path]"; exit 2; fi
ast-grep scan --config "$SG" "$PATH_"
echo "codemod scan done (review diff before applying --update-all)"
