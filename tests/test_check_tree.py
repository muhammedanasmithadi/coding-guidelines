"""Tests for scripts/check_tree gate logic."""

from __future__ import annotations

import datetime as dt
import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

from check_tree import (  # noqa: E402
    check_docs_examples,
    check_examples_linked,
    check_files,
    check_version,
    check_waivers,
    main,
)


def make_tree(tmp: pathlib.Path) -> pathlib.Path:
    (tmp / "docs" / "languages").mkdir(parents=True)
    (tmp / "checks").mkdir()
    (tmp / "examples" / "good-vs-bad").mkdir(parents=True)
    (tmp / "waivers").mkdir()
    (tmp / "VERSION").write_text("0.6.0\n")
    (tmp / "CHANGELOG.md").write_text("## [0.6.0] - 2026-10-10\n")
    (tmp / "docs" / "a.md").write_text("# A\n\n## Examples\n- x\n")
    (tmp / "docs" / "languages" / "b.md").write_text("# B\n\n## Examples\n- y\n")
    (tmp / "examples" / "good-vs-bad" / "e.md").write_text("# E\n")
    (tmp / "docs" / "a.md").write_text("# A\n\n## Examples\n- e.md\n")
    future = (dt.date.today() + dt.timedelta(days=10)).isoformat()
    waivers = [
        {
            "id": "W1",
            "rule": "r",
            "reason": "t",
            "owner": "@t",
            "expires": future,
            "issue": "https://example.com/1",
        }
    ]
    (tmp / "waivers" / "active.yml").write_text(yaml.safe_dump(waivers))
    return tmp


def test_clean_tree_ok(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    assert main(root) == 0


def test_detects_problems(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / "bad.md").write_text("x")  # outside docs/, ignored by docs rule
    (root / "docs" / "empty.md").write_text("")
    (root / "docs" / "nul.md").write_bytes(b"a\x00b")
    (root / "VERSION").write_text("9.9.9\n")
    assert check_files(root) != []
    assert check_version(root) != []
    assert main(root) == 1


def test_orphan_and_missing_examples(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / "examples" / "good-vs-bad" / "orphan.md").write_text("# O\n")
    (root / "docs" / "bare.md").write_text("# bare, no section\n")
    assert check_examples_linked(root) != []
    assert check_docs_examples(root) != []


def test_bad_waivers_fail(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    past = (dt.date.today() - dt.timedelta(days=1)).isoformat()
    (root / "waivers" / "active.yml").write_text(
        yaml.safe_dump(
            [
                {
                    "id": "W2",
                    "rule": "r",
                    "reason": "t",
                    "owner": "@t",
                    "expires": past,
                    "issue": "https://example.com/2",
                }
            ]
        )
    )
    assert check_waivers(root) != []
