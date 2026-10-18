"""Tests for scripts/check_version_drift gate logic."""

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

from check_version_drift import main  # noqa: E402


def make_root(tmp: pathlib.Path) -> pathlib.Path:
    (tmp / "enforce" / "python").mkdir(parents=True)
    (tmp / "requirements-ci.txt").write_text("ruff==0.17.0\n")
    pkg = {"version": "0.6.0", "devDependencies": {"oxfmt": "0.73.0"}}
    (tmp / "package.json").write_text(json.dumps(pkg))
    (tmp / ".python-version").write_text("3.14.8\n")
    (tmp / ".nvmrc").write_text("24.22.0\n")
    (tmp / "VERSION").write_text("0.6.0\n")
    (tmp / "CHANGELOG.md").write_text("## [0.6.0]\n")
    pyproject = 'target-version = "py314"\n'
    (tmp / "enforce" / "python" / "pyproject.toml").write_text(pyproject)
    return tmp


def test_clean_drift_ok(tmp_path: pathlib.Path) -> None:
    root = make_root(tmp_path)
    assert main(root) == 0


def test_pyproject_drift_fails(tmp_path: pathlib.Path) -> None:
    root = make_root(tmp_path)
    bad = 'target-version = "py313"\n'
    (root / "enforce" / "python" / "pyproject.toml").write_text(bad)
    assert main(root) == 1


def test_pinned_tool_drift_fails(tmp_path: pathlib.Path) -> None:
    root = make_root(tmp_path)
    (root / "Makefile").write_text("ruff==0.16.0\n")
    assert main(root) == 1
