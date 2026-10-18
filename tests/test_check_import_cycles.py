"""Tests for scripts/check_import_cycles gate logic."""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

from check_import_cycles import main  # noqa: E402


def make_pkg(root: pathlib.Path) -> pathlib.Path:
    (root / "src").mkdir()
    (root / "src" / "a.py").write_text("import src.b\n")
    (root / "src" / "b.py").write_text("import src.a\n")
    return root


def test_clean_ok(tmp_path: pathlib.Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "a.py").write_text("x = 1\n")
    assert main(tmp_path, ["src"]) == 0


def test_cycle_fails(tmp_path: pathlib.Path) -> None:
    make_pkg(tmp_path)
    assert main(tmp_path, ["src"]) == 1
