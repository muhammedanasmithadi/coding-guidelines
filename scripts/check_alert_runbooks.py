"""Ensure alerting rules reference a runbook when present."""

from __future__ import annotations

import argparse
import pathlib
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    print("pyyaml missing: pip install pyyaml")
    sys.exit(2)

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _alerts(data: object) -> list[dict[str, object]]:
    found: list[dict[str, object]] = []
    if isinstance(data, dict):
        groups = data.get("groups")
        if isinstance(groups, list):
            for group in groups:
                if isinstance(group, dict):
                    rules = group.get("rules")
                    if isinstance(rules, list):
                        for rule in rules:
                            if isinstance(rule, dict) and "alert" in rule:
                                found.append(rule)
    return found


def main(root: pathlib.Path = ROOT) -> int:
    problems: list[str] = []
    checked = 0
    for path in root.rglob("*.yml"):
        skip = (".git", "node_modules", ".venv", "__pycache__")
        if any(part in path.parts for part in skip):
            continue
        try:
            data = yaml.safe_load(path.read_text())
        except yaml.YAMLError:
            continue
        alerts = _alerts(data)
        if not alerts:
            continue
        checked += 1
        for alert in alerts:
            annotations = alert.get("annotations")
            has_runbook = False
            if isinstance(annotations, dict):
                has_runbook = any("runbook" in str(key).lower() for key in annotations)
            if not has_runbook:
                name = alert.get("alert", "?")
                rel = path.relative_to(root).as_posix()
                problems.append(f"{rel}: alert {name} missing runbook annotation")
    if problems:
        for p in problems:
            print(p)
        return 1
    print(f"alert runbooks ok ({checked} files)")
    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT))
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    sys.exit(main(pathlib.Path(args.root)))
