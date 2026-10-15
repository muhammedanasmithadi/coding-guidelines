"""Print the curated docs/checks for a task type from agent-context-map.yml."""

from __future__ import annotations

import pathlib
import sys

try:
    import yaml
except ImportError as err:  # pragma: no cover
    raise SystemExit("pyyaml missing: pip install pyyaml") from err  # noqa: TRY003

ROOT = pathlib.Path(__file__).resolve().parents[1]
VALID = {
    "feature",
    "api",
    "prod",
    "data",
    "event",
    "frontend",
    "security",
    "build",
    "realtime",
}


def main() -> int:
    task = sys.argv[1] if len(sys.argv) > 1 else ""
    if task not in VALID:
        print("usage: agent-context.py <" + "|".join(sorted(VALID)) + ">")
        return 2
    cfg = yaml.safe_load((ROOT / "agent-context-map.yml").read_text())
    for rel in cfg[task]:
        print(ROOT / rel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
