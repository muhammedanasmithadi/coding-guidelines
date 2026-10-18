"""Digest open standard-feedback issues into a summary issue."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from typing import Any


def list_feedback_issues() -> list[dict[str, Any]]:
    cmd = [
        "gh",
        "issue",
        "list",
        "--label",
        "standard-feedback",
        "--state",
        "open",
        "--json",
        "number,title,url",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "gh issue list failed")
    loaded: object = json.loads(result.stdout or "[]")
    if not isinstance(loaded, list):
        return []
    return [item for item in loaded if isinstance(item, dict)]


def build_body(issues: list[dict[str, Any]]) -> str:
    if not issues:
        return "No open standard-feedback issues."
    lines = ["# Standard feedback digest", "", f"Open items: {len(issues)}", ""]
    for issue in issues:
        lines.append(f"- #{issue['number']} {issue['title']} — {issue.get('url', '')}")
    return "\n".join(lines)


def main(dry_run: bool = False) -> int:
    issues = list_feedback_issues()
    body = build_body(issues)
    if dry_run:
        print(body)
        return 0
    if not issues:
        print("no feedback to digest")
        return 0
    cmd = [
        "gh",
        "issue",
        "create",
        "--title",
        "Standard feedback digest",
        "--body",
        body,
        "--label",
        "standard-feedback",
    ]
    subprocess.run(cmd, check=True)
    print("digest created")
    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    try:
        sys.exit(main(args.dry_run))
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
