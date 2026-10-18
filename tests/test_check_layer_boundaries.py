"""Tests for scripts/check_layer_boundaries gate logic."""

import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

from check_layer_boundaries import main  # noqa: E402


def make_layers(root: pathlib.Path) -> None:
    (root / "src" / "domain").mkdir(parents=True)
    (root / "src" / "app").mkdir(parents=True)
    (root / "src" / "domain" / "m.py").write_text("x = 1\n")
    (root / "src" / "app" / "m.py").write_text("import src.domain.m\n")
    cfg = {
        "layers": [
            {"name": "domain", "path": "src/domain"},
            {"name": "app", "path": "src/app"},
        ],
        "rules": {"domain": [], "app": ["domain"]},
    }
    (root / "layers.yml").write_text(yaml.safe_dump(cfg))


def test_clean_ok(tmp_path: pathlib.Path) -> None:
    make_layers(tmp_path)
    assert main(tmp_path) == 0


def test_violation_fails(tmp_path: pathlib.Path) -> None:
    make_layers(tmp_path)
    (tmp_path / "src" / "domain" / "m.py").write_text("import src.app.m\n")
    assert main(tmp_path) == 1


def test_no_config_ok(tmp_path: pathlib.Path) -> None:
    assert main(tmp_path) == 0
