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


def test_relative_cycle(tmp_path: pathlib.Path) -> None:
    pkg = tmp_path / "src" / "pkg"
    pkg.mkdir(parents=True)
    (pkg / "__init__.py").write_text("")
    (pkg / "a.py").write_text("from . import b\n")
    (pkg / "b.py").write_text("from . import a\n")
    assert main(tmp_path, ["src"]) == 1


def test_init_module(tmp_path: pathlib.Path) -> None:
    pkg = tmp_path / "src" / "pkg"
    pkg.mkdir(parents=True)
    (pkg / "__init__.py").write_text("x = 1\n")
    assert main(tmp_path, ["src"]) == 0


def test_syntax_error_skipped(tmp_path: pathlib.Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "bad.py").write_text("def (\n")
    assert main(tmp_path, ["src"]) == 0


def test_no_paths_ok(tmp_path: pathlib.Path) -> None:
    assert main(tmp_path) == 0


def test_cli_entrypoint(tmp_path: pathlib.Path) -> None:
    import subprocess
    import sys

    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "a.py").write_text("x = 1\n")
    result = subprocess.run(
        [
            sys.executable,
            str(
                pathlib.Path(__file__).resolve().parents[1]
                / "scripts"
                / "check_import_cycles.py"
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
