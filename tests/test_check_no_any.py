"""Tests for scripts/check_no_any gate logic."""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

from check_no_any import main  # noqa: E402


def test_clean_ok(tmp_path: pathlib.Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "m.py").write_text("def f(x: int) -> int:\n    return x\n")
    assert main(tmp_path, ["src"]) == 0


def test_bare_any_fails(tmp_path: pathlib.Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "m.py").write_text("def f(x: Any) -> Any:\n    return x\n")
    assert main(tmp_path, ["src"]) == 1


def test_generic_any_ok(tmp_path: pathlib.Path) -> None:
    (tmp_path / "src").mkdir()
    code = "from typing import Any\ndef f(x: list[Any]) -> list[Any]:\n    return x\n"
    (tmp_path / "src" / "m.py").write_text(code)
    assert main(tmp_path, ["src"]) == 0
