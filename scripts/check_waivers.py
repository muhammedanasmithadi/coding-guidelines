"""Fail CI on expired or over-long waivers in waivers/active.yml."""

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
MAX_DAYS = 90  # TEAM CHOICE: waiver may extend at most 90d past today


def load_entries(path: pathlib.Path) -> list[dict]:
    if not path.exists():
        return []
    try:
        data = yaml.safe_load(path.read_text())
    except yaml.YAMLError as e:
        raise ValueError(f"invalid YAML: {e}") from e
    if data is None:
        return []
    if not isinstance(data, list):
        raise ValueError("top level must be a list")
    for w in data:
        if not isinstance(w, dict):
            raise ValueError(f"entry must be a mapping: {w!r}")
    return data


def _expiry(w: dict) -> dt.date | None:
    if "expires" not in w:
        return None
    return dt.date.fromisoformat(str(w["expires"]))


def find_expired(path: pathlib.Path, today: dt.date) -> list[tuple[str, str]]:
    expired = []
    for w in load_entries(path):
        exp = _expiry(w)
        if exp is not None and exp < today:
            expired.append((w.get("id", "?"), str(w.get("expires"))))
    return expired


def find_invalid(path: pathlib.Path, today: dt.date) -> list[str]:
    problems = []
    for w in load_entries(path):
        wid = w.get("id", "?")
        if not w.get("owner"):
            problems.append(f"{wid}: missing owner")
        if not w.get("rule"):
            problems.append(f"{wid}: missing rule")
        if "expires" not in w:
            problems.append(f"{wid}: missing expires")
            continue
        try:
            exp = dt.date.fromisoformat(str(w["expires"]))
        except ValueError:
            problems.append(f"{wid}: bad expires date")
            continue
        if (exp - today).days > MAX_DAYS:
            problems.append(f"{wid}: exceeds {MAX_DAYS}d max")
    return problems


def main(path: pathlib.Path = DEFAULT_PATH) -> int:
    if not path.exists():
        print("no waivers file, ok")
        return 0
    today = dt.date.today()
    expired = find_expired(path, today)
    invalid = find_invalid(path, today)
    if expired:
        print(f"expired waivers: {expired}")
    if invalid:
        print(f"invalid waivers: {invalid}")
    if expired or invalid:
        return 1
    print("waivers ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
