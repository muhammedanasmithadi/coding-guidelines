"""Tests for scripts/check-waivers gate logic."""

from __future__ import annotations

import datetime as dt
import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

from check_waivers import find_expired, main  # noqa: E402


def write_waivers(tmp: pathlib.Path, entries: list[dict]) -> pathlib.Path:
    wdir = tmp / "waivers"
    wdir.mkdir(parents=True, exist_ok=True)
    path = wdir / "active.yml"
    path.write_text(yaml.safe_dump(entries))
    return path


def test_missing_file_ok(tmp_path: pathlib.Path) -> None:
    assert main(tmp_path / "waivers" / "active.yml") == 0
    assert find_expired(tmp_path / "nope.yml", dt.date.today()) == []


def test_future_waiver_passes(tmp_path: pathlib.Path) -> None:
    future = (dt.date.today() + dt.timedelta(days=30)).isoformat()
    path = write_waivers(
        tmp_path,
        [
            {
                "id": "WAIV-T",
                "rule": "example",
                "reason": "t",
                "owner": "@t",
                "expires": future,
                "issue": "https://example.com/1",
            }
        ],
    )
    assert find_expired(path, dt.date.today()) == []
    assert main(path) == 0


def test_expired_fails(tmp_path: pathlib.Path) -> None:
    past = (dt.date.today() - dt.timedelta(days=1)).isoformat()
    path = write_waivers(
        tmp_path,
        [
            {
                "id": "WAIV-E",
                "rule": "example",
                "reason": "t",
                "owner": "@t",
                "expires": past,
                "issue": "https://example.com/2",
            }
        ],
    )
    assert find_expired(path, dt.date.today()) == [("WAIV-E", past)]
    assert main(path) == 1
