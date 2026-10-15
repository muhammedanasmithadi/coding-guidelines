"""Tests for scripts/check_tree gate logic."""

from __future__ import annotations

import datetime as dt
import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

from check_tree import (  # noqa: E402
    check_dangling,
    check_docs_examples,
    check_examples_linked,
    check_files,
    check_version,
    check_waivers,
    main,
)


def write_waivers(root: pathlib.Path, entries: list[dict]) -> None:
    wdir = root / "waivers"
    wdir.mkdir(parents=True, exist_ok=True)
    (wdir / "active.yml").write_text(yaml.safe_dump(entries))


def make_tree(tmp: pathlib.Path) -> pathlib.Path:
    (tmp / "docs" / "languages").mkdir(parents=True)
    (tmp / "checks").mkdir()
    (tmp / "examples" / "good-vs-bad").mkdir(parents=True)
    (tmp / "VERSION").write_text("0.6.0\n")
    (tmp / "CHANGELOG.md").write_text("## [0.6.0] - 2026-10-10\n")
    (tmp / "package.json").write_text('{"version": "0.6.0"}\n')
    (tmp / "docs" / "a.md").write_text("# A\n\nSources: x\n\n## Examples\n- e.md\n")
    (tmp / "docs" / "languages" / "b.md").write_text("# B\n\nSources: y\n\n## Examples\n- y\n")
    (tmp / "examples" / "good-vs-bad" / "e.md").write_text("# E\n")
    future = (dt.datetime.now(dt.UTC).date() + dt.timedelta(days=10)).isoformat()
    write_waivers(
        tmp,
        [
            {
                "id": "W1",
                "rule": "r",
                "reason": "t",
                "owner": "@t",
                "expires": future,
                "issue": "https://example.com/1",
            }
        ],
    )
    return tmp


def test_clean_tree_ok(tmp_path: pathlib.Path) -> None:
    assert main(make_tree(tmp_path)) == 0


def test_nul_empty_and_version_problems(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / "docs" / "empty.md").write_text("")
    (root / "docs" / "nul.md").write_bytes(b"a\x00b")
    (root / "VERSION").write_text("9.9.9\n")
    assert any("empty" in p for p in check_files(root))
    assert any("NUL" in p for p in check_files(root))
    assert check_version(root) != []
    assert main(root) == 1


def test_generated_artifacts_skipped(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / ".coverage").write_bytes(b"\x00sqlite")
    (root / "node_modules" / "pkg").mkdir(parents=True)
    (root / "node_modules" / "pkg" / "b.node").write_bytes(b"\x00bin")
    assert check_files(root) == []


def test_archives_skipped(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / "bundle.tar.gz").write_bytes(b"\x00data")
    assert check_files(root) == []


def test_stem_substring_does_not_satisfy_link(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / "examples" / "good-vs-bad" / "orphan.md").write_text("# O\n")
    (root / "docs" / "a.md").write_text("# A\n\n## Examples\norphans everywhere\n")
    orphans = check_examples_linked(root)
    assert "examples/good-vs-bad/orphan.md: orphaned" in orphans
    assert "examples/good-vs-bad/e.md: orphaned" in orphans
    (root / "docs" / "a.md").write_text("# A\n\n## Examples\n- e.md\n- orphan.md\n")
    assert check_examples_linked(root) == []


def test_hash_header_does_not_count(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / "docs" / "bare.md").write_text("# bare\n\n### Examples\n- e.md\n")
    assert check_docs_examples(root) == ["docs/bare.md: no ## Examples"]


def test_dangling_reference(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / "docs" / "a.md").write_text(
        "# A\n\n## Examples\n- examples/good-vs-bad/ghost.md\n- e.md\n"
    )
    dangling = "docs/a.md: dangling `examples/good-vs-bad/ghost.md`"
    assert check_dangling(root) == [dangling]


def test_package_version_enforced(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / "package.json").write_text('{"version": "0.0.1"}\n')
    assert any("package.json" in p for p in check_version(root))


def test_bad_waivers_fail(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    past = (dt.datetime.now(dt.UTC).date() - dt.timedelta(days=1)).isoformat()
    write_waivers(
        tmp_path,
        [
            {
                "id": "W2",
                "rule": "r",
                "reason": "t",
                "owner": "@t",
                "expires": past,
                "issue": "https://example.com/2",
            }
        ],
    )
    assert check_waivers(root) != []
    (root / "waivers" / "active.yml").write_text("::: not yaml [[[\n- {id: x}\n")
    assert check_waivers(root) != []


def test_baseline_artifacts_skipped(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    wdir = root / "waivers"
    wdir.mkdir(parents=True, exist_ok=True)
    (wdir / "baseline.ruff.json").write_bytes(b"\x00bad")
    assert check_files(root) == []


def test_oxlint_directive_allowed(tmp_path: pathlib.Path) -> None:
    from check_tree import check_comments

    root = make_tree(tmp_path)
    (root / "w.mjs").write_text('const u = 1;\n// oxlint-disable-next-line no-console\n')
    problems = check_comments(root)
    assert not [p for p in problems if "w.mjs:2" in p]


def test_comments_banned_except_directives(tmp_path: pathlib.Path) -> None:
    from check_tree import check_comments

    root = make_tree(tmp_path)
    (root / "x.py").write_text("import os  # noqa: F401\n# explain\n")
    (root / "y.sh").write_text("#!/usr/bin/env bash\n# usage note\n")
    (root / "z.yaml").write_text("a: 1  # trailing\n")
    (root / "w.mjs").write_text('const u = "https://x.y/z";\n// narrate\n')
    problems = check_comments(root)
    assert "x.py:2: comment" in problems
    assert "y.sh:2: comment" in problems
    assert "z.yaml:1: comment" in problems
    assert "w.mjs:2: comment" in problems
    assert not [p for p in problems if "x.py:1" in p]


def test_missing_source_fails(tmp_path: pathlib.Path) -> None:
    from check_tree import check_sources

    root = make_tree(tmp_path)
    (root / "docs" / "a.md").write_text("# A\n\n## Examples\n- e.md\n")
    assert any("no Sources" in p for p in check_sources(root))


def test_cli_root_override(tmp_path: pathlib.Path) -> None:
    import subprocess

    root = make_tree(tmp_path)
    script = pathlib.Path(__file__).resolve().parents[1]
    script = script / "scripts" / "check_tree.py"
    proc = subprocess.run(
        [sys.executable, str(script), str(root)], capture_output=True, text=True
    )
    assert proc.returncode == 0, proc.stdout
