from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKIP_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "__pycache__",
    ".ruff_cache",
    ".pytest_cache",
    "tests",
}


def _canonical_versions(root: pathlib.Path = ROOT) -> dict[str, str]:
    versions: dict[str, str] = {}
    req = root / "requirements-ci.txt"
    for line in req.read_text().splitlines():
        line = line.strip()
        if "==" in line and not line.startswith("#"):
            name, version = line.split("==", 1)
            versions[name.strip()] = version.strip()
    pkg = json.loads((root / "package.json").read_text())
    for name, version in (pkg.get("devDependencies") or {}).items():
        versions[name] = version.lstrip("^~")
    python = (root / ".python-version").read_text().strip()
    node = (root / ".nvmrc").read_text().strip()
    versions["python"] = python
    versions["node"] = node
    return versions


PATTERNS = {
    "ruff": re.compile(r"ruff==([0-9][0-9.]*)"),
    "mypy": re.compile(r"mypy==([0-9][0-9.]*)"),
    "semgrep": re.compile(r"semgrep==([0-9][0-9.]*)"),
    "oxfmt": re.compile(r"oxfmt@([0-9][0-9.]*)"),
    "oxlint": re.compile(r"oxlint@([0-9][0-9.]*)"),
    "cspell": re.compile(r"cspell@([0-9][0-9.]*)"),
}


def _candidate_files_root(root: pathlib.Path = ROOT) -> list[pathlib.Path]:
    files = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix in {".pyc"}:
            continue
        try:
            path.read_text()
        except UnicodeDecodeError, OSError:
            continue
        files.append(path)
    return files


def check_pyproject_target(root: pathlib.Path, python_version: str) -> list[str]:
    pyproject = root / "enforce" / "python" / "pyproject.toml"
    text = pyproject.read_text()
    match = re.search(r'^target-version\s*=\s*"py(\d+)"', text, re.MULTILINE)
    if not match:
        return ["pyproject target-version missing"]
    major, minor = python_version.split(".")[:2]
    expected = f"{major}{minor}"
    if match.group(1) != expected:
        found = match.group(1)
        return [f"pyproject target-version py{found} != python {python_version}"]
    return []


def main(root: pathlib.Path = ROOT) -> int:
    versions = _canonical_versions(root)
    problems: list[str] = []
    problems.extend(check_pyproject_target(root, versions["python"]))

    for path in _candidate_files_root(root):
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text()
        except OSError:
            continue
        for tool, pattern in PATTERNS.items():
            canonical = versions.get(tool)
            if canonical is None:
                continue
            for match in pattern.finditer(text):
                found = match.group(1)
                if found != canonical:
                    problems.append(f"{rel}: {tool} {found} != {canonical}")

    if problems:
        for p in problems:
            print(p)
        return 1
    print("version drift ok")
    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT))
    args = parser.parse_args()
    sys.exit(main(pathlib.Path(args.root)))
