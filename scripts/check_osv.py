"""Run osv-scanner when installed (advisory)."""

from __future__ import annotations

import argparse
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main(root: pathlib.Path = ROOT) -> int:
    if shutil.which("osv-scanner") is None:
        print("osv-scanner not installed, skipping")
        return 0
    result = subprocess.run(
        ["osv-scanner", "scan", "--lockfile", str(root / "package-lock.json")],
        cwd=root,
        check=False,
    )
    if result.returncode != 0:
        print("osv-scanner found vulnerabilities", file=sys.stderr)
        return 1
    print("osv-scanner ok")
    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT))
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    sys.exit(main(pathlib.Path(args.root)))
