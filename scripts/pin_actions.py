from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MIN_ACTION_PARTS = 2
SHA_LENGTH = 40
USES_RE = re.compile(r"^(\s*-?\s*uses:\s*)([^@\s]+)@(\S+)(.*)$")


def split_action(action: str) -> tuple[str, str]:
    parts = action.split("/")
    if len(parts) >= MIN_ACTION_PARTS:
        return "/".join(parts[:2]), "/".join(parts[2:])
    return action, ""


def resolve(owner_repo: str, ref: str) -> str | None:
    result = subprocess.run(
        ["gh", "api", f"repos/{owner_repo}/commits/{ref}", "--jq", ".sha"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    sha = result.stdout.strip()
    if len(sha) == SHA_LENGTH:
        return sha
    return None


def main(root: pathlib.Path = ROOT) -> int:
    for path in (root / ".github" / "workflows").glob("*.yml"):
        lines = path.read_text().splitlines()
        changed = False
        new_lines = []
        for line in lines:
            match = USES_RE.match(line)
            if match and not re.search(r"@[0-9a-f]{40}", match.group(3)):
                prefix = match.group(1)
                action = match.group(2)
                ref = match.group(3)
                suffix = match.group(4)
                repo, subpath = split_action(action)
                sha = resolve(repo, ref)
                if sha is None:
                    print(f"could not resolve {action}@{ref}", file=sys.stderr)
                    new_lines.append(line)
                    continue
                new_action = action if not subpath else f"{repo}/{subpath}"
                new_lines.append(f"{prefix}{new_action}@{sha}{suffix}")
                changed = True
            else:
                new_lines.append(line)
        if changed:
            path.write_text("\n".join(new_lines) + "\n")
            print(f"pinned {path.relative_to(root)}")
    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT))
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    sys.exit(main(pathlib.Path(args.root)))
