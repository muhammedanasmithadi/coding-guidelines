import pathlib
import subprocess
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
    code = "from typing import Any\ndef f(x: list[Any]) -> list[Any]:\n    return x\n"
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "m.py").write_text(code)
    assert main(tmp_path, ["src"]) == 0


def test_syntax_error_skipped(tmp_path: pathlib.Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "bad.py").write_text("def (\n")
    assert main(tmp_path, ["src"]) == 0


def test_no_paths_ok(tmp_path: pathlib.Path) -> None:
    assert main(tmp_path) == 0


def test_async_and_vararg(tmp_path: pathlib.Path) -> None:
    code = (
        "from typing import Any\n"
        "async def f(*args: Any, **kwargs: Any) -> Any:\n"
        "    return None\n"
    )
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "m.py").write_text(code)
    assert main(tmp_path, ["src"]) == 1


def test_cli_entrypoint(tmp_path: pathlib.Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "m.py").write_text("def f(x: int) -> int:\n    return x\n")
    result = subprocess.run(
        [
            sys.executable,
            str(
                pathlib.Path(__file__).resolve().parents[1]
                / "scripts"
                / "check_no_any.py"
            ),
            "--root",
            str(tmp_path),
            "--paths",
            "src",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
