"""Fail when docs or checks change without a CHANGELOG entry."""

from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
WATCHED_PREFIXES = ("docs/", "checks/")


def changed_files(base: str, head: str, root: pathlib.Path = ROOT) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", base, head],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git diff failed")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def needs_changelog(files: list[str]) -> bool:
    return any(f.startswith(WATCHED_PREFIXES) for f in files)


def main(base: str = "HEAD~1", head: str = "HEAD", root: pathlib.Path = ROOT) -> int:
    files = changed_files(base, head, root)
    if not needs_changelog(files):
        print("changelog ok (no watched paths changed)")
        return 0
    if "CHANGELOG.md" in files:
        print("changelog ok")
        return 0
    watched = [f for f in files if f.startswith(WATCHED_PREFIXES)]
    print(f"CHANGELOG.md must be updated when these change: {watched}")
    return 1


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="HEAD~1")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--root", default=str(ROOT))
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    sys.exit(main(args.base, args.head, pathlib.Path(args.root)))
