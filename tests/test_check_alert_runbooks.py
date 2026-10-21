import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

from check_alert_runbooks import main  # noqa: E402


def test_no_alerts_ok(tmp_path: pathlib.Path) -> None:
    (tmp_path / "a.yml").write_text("foo: bar\n")
    assert main(tmp_path) == 0


def test_alert_without_runbook_fails(tmp_path: pathlib.Path) -> None:
    cfg = {"groups": [{"rules": [{"alert": "HighErrorRate", "expr": "x > 1"}]}]}
    (tmp_path / "alerts.yml").write_text(yaml.safe_dump(cfg))
    assert main(tmp_path) == 1


def test_alert_with_runbook_ok(tmp_path: pathlib.Path) -> None:
    cfg = {
        "groups": [
            {
                "rules": [
                    {
                        "alert": "HighErrorRate",
                        "expr": "x > 1",
                        "annotations": {"runbook_url": "http://x"},
                    }
                ]
            }
        ]
    }
    (tmp_path / "alerts.yml").write_text(yaml.safe_dump(cfg))
    assert main(tmp_path) == 0
