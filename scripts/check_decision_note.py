from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
WATCHED_PREFIXES = ("docs/", "checks/", "enforce/", "scripts/", ".github/workflows/")
RATIONALE_MARKERS = ("decision:", "rationale:", "adr-")


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


def watched(files: list[str]) -> list[str]:
    return [f for f in files if f.startswith(WATCHED_PREFIXES)]


def has_rationale(body: str) -> bool:
    lowered = body.lower()
    return any(marker in lowered for marker in RATIONALE_MARKERS)


def main(
    base: str = "HEAD~1",
    head: str = "HEAD",
    body_file: str | None = None,
    root: pathlib.Path = ROOT,
) -> int:
    files = changed_files(base, head, root)
    touched = watched(files)
    if not touched:
        print("decision note ok (no rule paths changed)")
        return 0
    body = ""
    if body_file:
        path = pathlib.Path(body_file)
        if path.exists():
            body = path.read_text()
    if has_rationale(body):
        print("decision note ok")
        return 0
    print(
        "PR body must carry the rationale for a change to these paths: "
        f"{touched}\n"
        "Add a 'Decision:' or 'Rationale:' section, or name the ADR."
    )
    return 1


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="HEAD~1")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--body-file", default=None)
    parser.add_argument("--root", default=str(ROOT))
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    sys.exit(main(args.base, args.head, args.body_file, pathlib.Path(args.root)))
