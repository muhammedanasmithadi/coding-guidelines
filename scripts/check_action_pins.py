from __future__ import annotations

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SHA_RE = re.compile(r"@[0-9a-f]{40}$")


def main(root: pathlib.Path = ROOT, strict: bool = False) -> int:
    problems: list[str] = []
    for path in (root / ".github" / "workflows").glob("*.yml"):
        for number, line in enumerate(path.read_text().splitlines(), 1):
            stripped = line.strip()
            if "uses:" not in stripped:
                continue
            value = stripped.split("uses:", 1)[1].strip()
            if "@" not in value:
                continue
            if not SHA_RE.search(value):
                rel = path.relative_to(root).as_posix()
                problems.append(f"{rel}:{number}: unpinned action {value}")
    if problems:
        for p in problems:
            print(p)
        return 1 if strict else 0
    print("action pins ok")
    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    sys.exit(main(pathlib.Path(args.root), args.strict))
