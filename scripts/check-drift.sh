#!/usr/bin/env bash
set -euo pipefail
# Compares local enforce/ against the released tag. Advisory until P0 rollout.
# Usage: scripts/check-drift.sh v0.5.0
TAG="${1:-}"
if [ -z "$TAG" ]; then echo "usage: check-drift.sh <tag>"; exit 2; fi
tmp=$(mktemp -d)
git archive "$TAG" enforce/ checks/ | tar -x -C "$tmp"
if diff -r -q "$tmp/enforce" enforce/ && diff -r -q "$tmp/checks" checks/; then
  echo "no drift vs $TAG"
else
  echo "drift vs $TAG detected (advisory)"
fi
rm -rf "$tmp"
