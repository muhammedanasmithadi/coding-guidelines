"""Fail CI on expired waivers in waivers/active.yml."""

from __future__ import annotations

import datetime as dt
import pathlib
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    print("pyyaml missing: pip install pyyaml")
    sys.exit(2)

DEFAULT_PATH = pathlib.Path(__file__).resolve().parents[1] / "waivers/active.yml"


def find_expired(path: pathlib.Path, today: dt.date) -> list[tuple[str, str]]:
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text()) or []
    expired = []
    for w in data:
        exp = dt.date.fromisoformat(str(w["expires"]))
        if exp < today:
            expired.append((w.get("id", "?"), str(w.get("expires"))))
    return expired


def main(path: pathlib.Path = DEFAULT_PATH) -> int:
    if not path.exists():
        print("no waivers file, ok")
        return 0
    expired = find_expired(path, dt.date.today())
    if expired:
        print(f"expired waivers: {expired}")
        return 1
    print("waivers ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
