#!/usr/bin/env bash

set -euo pipefail
mise install || true
pre-commit install || true
python3 --version; node --version
pre-commit run --all-files || true
make check
echo "bootstrap green"
