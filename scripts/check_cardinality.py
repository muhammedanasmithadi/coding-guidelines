"""Fail when forbidden high-cardinality labels appear in metric code."""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
FORBIDDEN = ("user_id", "order_id")
METRIC_HINT = re.compile(r"label|metric|counter|gauge|histogram", re.IGNORECASE)
SKIP_PARTS = (".git", "node_modules", ".venv", "__pycache__", "tests")
SUFFIXES = {".py", ".ts", ".tsx", ".js", ".go", ".rs"}


def scan_file(path: pathlib.Path, root: pathlib.Path) -> list[str]:
    problems: list[str] = []
    try:
        lines = path.read_text().splitlines()
    except OSError, UnicodeDecodeError:
        return problems
    rel = path.relative_to(root).as_posix()
    for number, line in enumerate(lines, 1):
        if not METRIC_HINT.search(line):
            continue
        for token in FORBIDDEN:
            if token in line:
                problems.append(f"{rel}:{number}: forbidden cardinality label {token}")
    return problems


def main(root: pathlib.Path = ROOT) -> int:
    problems: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in path.parts for part in SKIP_PARTS):
            continue
        if path.suffix not in SUFFIXES:
            continue
        problems.extend(scan_file(path, root))
    if problems:
        for p in problems:
            print(p)
        return 1
    print("cardinality ok")
    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT))
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    sys.exit(main(pathlib.Path(args.root)))
