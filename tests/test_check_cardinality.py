import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

from check_cardinality import main  # noqa: E402


def test_clean_ok(tmp_path: pathlib.Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "m.py").write_text("x = 1\n")
    assert main(tmp_path) == 0


def test_forbidden_label_fails(tmp_path: pathlib.Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "m.py").write_text("metric = counter.labels(user_id=u)\n")
    assert main(tmp_path) == 1
