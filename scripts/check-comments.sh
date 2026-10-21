#!/usr/bin/env bash

set -euo pipefail

roots=("$@")
if [ ${#roots[@]} -eq 0 ]; then
  roots=(".")
fi

status=0
for root in "${roots[@]}"; do
  [ -d "$root" ] || continue
  while IFS= read -r file; do
    case "$file" in
      */target/* | */node_modules/* | */.git/*) continue ;;
    esac
    hits=$(grep -nE '(^|[^:"])//|/\*|^\s*#' "$file" | grep -vE '(noqa|pragma|nolint|eslint-disable|oxlint-disable|https?://)' || true)
    if [ -n "$hits" ]; then
      echo "$file:"
      echo "$hits" | sed 's/^/  /'
      status=1
    fi
  done < <(find "$root" -type f \( -name '*.rs' -o -name '*.kt' -o -name '*.c' -o -name '*.h' -o -name '*.go' \) 2>/dev/null)
done

if [ "$status" -eq 0 ]; then
  echo "no comments found (advisory)"
fi
exit 0
