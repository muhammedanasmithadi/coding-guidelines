"""Fail CI when repo hygiene slips: NULs, empties, version drift, orphaned examples."""

from __future__ import annotations

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import datetime as dt  # noqa: E402

from check_waivers import find_expired, find_invalid  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".ruff_cache", ".pytest_cache", "__pycache__"}
TEXT_SUFFIXES = {".md", ".yml", ".yaml", ".json", ".toml", ".mjs", ".py", ".sh"}
VERSION_RE = re.compile(r"^## \[([0-9]+\.[0-9]+\.[0-9]+)\]", re.MULTILINE)


def check_files(root: pathlib.Path = ROOT) -> list[str]:
    problems = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(d in p.parts for d in SKIP_DIRS):
            continue
        b = p.read_bytes()
        if b"\x00" in b:
            problems.append(f"{p.relative_to(root)}: NUL bytes")
        elif len(b) == 0 and p.suffix in TEXT_SUFFIXES:
            problems.append(f"{p.relative_to(root)}: empty")
    return problems


def check_version(root: pathlib.Path = ROOT) -> list[str]:
    version = (root / "VERSION").read_text().strip()
    match = VERSION_RE.search((root / "CHANGELOG.md").read_text())
    if not match:
        return ["CHANGELOG.md: no ## [x.y.z] entry"]
    if match.group(1) != version:
        return [f"VERSION {version} != CHANGELOG {match.group(1)}"]
    return []


def check_examples_linked(root: pathlib.Path = ROOT) -> list[str]:
    pool = ""
    for base in ("docs", "checks", "README.md", ".github"):
        p = root / base
        if p.is_file():
            pool += p.read_text()
        elif p.is_dir():
            for f in p.rglob("*.md"):
                pool += f.read_text()
    orphans = []
    for f in (root / "examples" / "good-vs-bad").glob("*.md"):
        if f.name == "README.md":
            continue
        if f.name not in pool and f.stem not in pool:
            orphans.append(f"examples/good-vs-bad/{f.name}: orphaned")
    return orphans


def check_docs_examples(root: pathlib.Path = ROOT) -> list[str]:
    missing = []
    for base in ("docs", "docs/languages"):
        for f in sorted((root / base).glob("*.md")):
            if "## Examples" not in f.read_text():
                missing.append(f"{f.relative_to(root)}: no ## Examples")
    return missing


def check_waivers(root: pathlib.Path = ROOT) -> list[str]:
    path = root / "waivers" / "active.yml"
    today = dt.date.today()
    problems = [f"waivers: {e}" for e in find_expired(path, today)]
    problems += [f"waivers: {e}" for e in find_invalid(path, today)]
    return problems


def main(root: pathlib.Path = ROOT) -> int:
    problems = (
        check_files(root)
        + check_version(root)
        + check_examples_linked(root)
        + check_docs_examples(root)
        + check_waivers(root)
    )
    if problems:
        print("\n".join(problems))
        return 1
    print("tree ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
