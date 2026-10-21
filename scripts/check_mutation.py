from __future__ import annotations

import argparse
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main(root: pathlib.Path = ROOT) -> int:
    if shutil.which("mutmut") is None:
        print("mutmut not installed, skipping")
        return 0
    result = subprocess.run(
        ["mutmut", "run", "--paths-to-mutate", "scripts"],
        cwd=root,
        check=False,
    )
    if result.returncode != 0:
        print("mutation testing found survivors", file=sys.stderr)
        return 1
    print("mutation testing ok")
    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT))
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    sys.exit(main(pathlib.Path(args.root)))
