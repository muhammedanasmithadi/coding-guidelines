"""Tests for scripts/check_perf_budgets gate logic."""

import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

from check_perf_budgets import main  # noqa: E402


def test_no_config_ok(tmp_path: pathlib.Path) -> None:
    assert main(tmp_path) == 0


def test_valid_config_ok(tmp_path: pathlib.Path) -> None:
    cfg = {
        "budgets": {
            "api_p95_ms": 300,
            "api_p99_ms": 800,
            "bundle_kb": 200,
            "db_queries_per_request": 5,
        }
    }
    (tmp_path / "performance-budgets.yml").write_text(yaml.safe_dump(cfg))
    assert main(tmp_path) == 0


def test_invalid_budget_fails(tmp_path: pathlib.Path) -> None:
    cfg = {
        "budgets": {
            "api_p95_ms": 0,
            "api_p99_ms": 800,
            "bundle_kb": 200,
            "db_queries_per_request": 5,
        }
    }
    (tmp_path / "performance-budgets.yml").write_text(yaml.safe_dump(cfg))
    assert main(tmp_path) == 1
