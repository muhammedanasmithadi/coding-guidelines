"""Run oasdiff breaking-change check when a baseline spec exists."""

from __future__ import annotations

import argparse
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main(root: pathlib.Path = ROOT) -> int:
    oasdiff = shutil.which("oasdiff")
    base = root / "openapi.baseline.yaml"
    current = root / "openapi.yaml"
    if oasdiff is None:
        print("oasdiff not installed, skipping")
        return 0
    if not base.exists() or not current.exists():
        print("no openapi baseline/current, skipping")
        return 0
    result = subprocess.run(
        [oasdiff, "breaking", str(base), str(current)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        return 1
    print("openapi breaking changes: none")
    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT))
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    sys.exit(main(pathlib.Path(args.root)))
