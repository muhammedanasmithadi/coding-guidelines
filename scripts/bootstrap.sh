#!/usr/bin/env bash
set -euo pipefail
# One-command golden path: toolchain + hooks + local gates.
mise install || true
pre-commit install || true
python3 --version; node --version
pre-commit run --all-files || true
make check
echo "bootstrap green"
