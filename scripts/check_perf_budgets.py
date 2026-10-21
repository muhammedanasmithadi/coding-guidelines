from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    print("pyyaml missing: pip install pyyaml")
    sys.exit(2)

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONFIG_NAMES = (
    "performance-budgets.yml",
    "checks/performance-budgets.yml",
    "enforce/performance-budgets.yml",
)
REQUIRED = ("api_p95_ms", "api_p99_ms", "bundle_kb", "db_queries_per_request")


def load_config(root: pathlib.Path) -> dict[str, Any] | None:
    for name in CONFIG_NAMES:
        path = root / name
        if path.exists():
            data = yaml.safe_load(path.read_text())
            if isinstance(data, dict):
                return data
    return None


def main(root: pathlib.Path = ROOT) -> int:
    config = load_config(root)
    if config is None:
        print("no performance budgets config, skipping")
        return 0
    budgets = config.get("budgets", {})
    if not isinstance(budgets, dict):
        print("budgets must be a mapping")
        return 1
    problems: list[str] = []
    for key in REQUIRED:
        if key not in budgets:
            problems.append(f"missing budget: {key}")
            continue
        value = budgets[key]
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
            problems.append(f"invalid budget {key}: {value!r}")
    if problems:
        for p in problems:
            print(p)
        return 1
    print("performance budgets ok")
    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT))
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    sys.exit(main(pathlib.Path(args.root)))
