#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import re
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
PYTHON_API = "https://endoflife.date/api/python.json"
NODE_API = "https://endoflife.date/api/nodejs.json"
MINIMUM_VERSION_PARTS = 2


class RuntimeVersionError(Exception): ...


def fetch_json(url: str) -> list[dict[str, object]]:
    with urllib.request.urlopen(url, timeout=30) as response:
        loaded = json.load(response)
    if not isinstance(loaded, list):
        raise RuntimeVersionError
    return loaded


def product_cycle(version: str) -> str:
    parts = version.strip().lstrip("v").split(".")
    if len(parts) < MINIMUM_VERSION_PARTS:
        raise RuntimeVersionError
    return ".".join(parts[:2])


def latest_version(url: str, cycle_value: str) -> str:
    for entry in fetch_json(url):
        if str(entry.get("cycle", "")) != cycle_value:
            continue
        latest = entry.get("latest")
        if latest is None:
            raise RuntimeVersionError
        return str(latest)
    raise RuntimeVersionError


def target_version_line(version: str) -> str:
    major, minor = version.split(".")[:2]
    return f"py{major}{minor}"


def write_version(path: pathlib.Path, latest: str) -> bool:
    current = path.read_text().strip() if path.exists() else ""
    if current == latest:
        return False
    path.write_text(latest + "\n")
    return True


def update_pyproject(py_version: str, dry_run: bool) -> bool:
    path = ROOT / "enforce" / "python" / "pyproject.toml"
    content = path.read_text()
    desired = f'target-version = "{target_version_line(py_version)}"'
    pattern = re.compile(r'^target-version\s*=\s*".*"$', re.MULTILINE)
    if not pattern.search(content):
        raise RuntimeVersionError
    new_content = pattern.sub(desired, content, count=1)
    if new_content == content:
        return False
    if not dry_run:
        path.write_text(new_content)
    return True


def bump(dry_run: bool, check_only: bool) -> int:
    python_path = ROOT / ".python-version"
    node_path = ROOT / ".nvmrc"
    current_python = python_path.read_text().strip()
    current_node = node_path.read_text().strip()
    python_minor = ".".join(current_python.split(".")[:2])
    node_major = current_node.split(".")[0]
    latest_python = latest_version(PYTHON_API, python_minor)
    latest_node = latest_version(NODE_API, node_major)
    python_changed = current_python != latest_python
    node_changed = current_node != latest_node
    pyproject_changed = update_pyproject(latest_python, dry_run=True)

    if check_only:
        print(f"python: current={current_python} latest={latest_python}")
        print(f"node: current={current_node} latest={latest_node}")
        return 1 if python_changed or node_changed or pyproject_changed else 0

    changed = False
    if python_changed and not dry_run:
        python_path.write_text(latest_python + "\n")
        changed = True
    if node_changed and not dry_run:
        node_path.write_text(latest_node + "\n")
        changed = True
    if pyproject_changed and not dry_run:
        update_pyproject(latest_python, dry_run=False)
        changed = True
    print(f"python: {current_python} -> {latest_python}")
    print(f"node: {current_node} -> {latest_node}")
    print("changed: true" if changed else "changed: false")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return bump(args.dry_run, args.check)


if __name__ == "__main__":
    raise SystemExit(main())
