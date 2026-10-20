"""Open a draft PR with AI-proposed guideline improvements (optional)."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def collect_context() -> str:
    parts = []
    freshness = subprocess.run(
        ["bash", str(ROOT / "scripts" / "check-freshness.sh")],
        capture_output=True,
        text=True,
        check=False,
    )
    parts.append("FRESHNESS REPORT:\n" + (freshness.stdout or "")[:4000])
    log = subprocess.run(
        ["git", "log", "--since=7 days ago", "--oneline"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    parts.append("RECENT COMMITS:\n" + (log.stdout or "")[:2000])
    return "\n\n".join(parts)


def call_openai(prompt: str, api_key: str, model: str) -> str:
    system_msg = "You are a technical editor for a coding guidelines repo."
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers=headers,
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data: object = json.loads(resp.read())
    if not isinstance(data, dict):
        raise TypeError("unexpected response")  # noqa: TRY003
    choices = data.get("choices")
    if not isinstance(choices, list) or not choices:
        raise ValueError("no choices")  # noqa: TRY003
    first = choices[0]
    if not isinstance(first, dict):
        raise TypeError("bad choice")  # noqa: TRY003
    message = first.get("message")
    if not isinstance(message, dict):
        raise TypeError("bad message")  # noqa: TRY003
    content = message.get("content")
    if not isinstance(content, str):
        raise TypeError("bad content")  # noqa: TRY003
    return content


def main(dry_run: bool = False) -> int:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        print("OPENAI_API_KEY not set; skipping AI docs draft.")
        return 0
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini").strip()
    context = collect_context()
    prompt = (
        "Propose 3-5 concrete, small improvements to the coding guidelines "
        "based on this context. Return Markdown with headings and rationale. "
        "Do not invent files that do not exist.\n\n" + context
    )
    content = call_openai(prompt, api_key, model)
    today = dt.datetime.now(dt.UTC).date().isoformat()
    proposal = f"# AI-proposed guideline improvements ({today})\n\n{content}\n"
    if dry_run:
        print(proposal)
        return 0

    branch = f"bot/ai-docs-draft-{dt.datetime.now(dt.UTC).strftime('%Y%m%d%H%M%S')}"
    subprocess.run(["git", "checkout", "-b", branch], cwd=ROOT, check=True)
    out_dir = ROOT / "proposals"
    out_dir.mkdir(exist_ok=True)
    today = dt.datetime.now(dt.UTC).date().isoformat()
    out_file = out_dir / f"ai-{today}.md"
    out_file.write_text(proposal)
    rel = str(out_file.relative_to(ROOT))
    subprocess.run(["git", "add", rel], cwd=ROOT, check=True)
    msg = "docs: AI-proposed guideline improvements (draft)"
    subprocess.run(["git", "commit", "-m", msg], cwd=ROOT, check=True)
    subprocess.run(["git", "push", "origin", branch], cwd=ROOT, check=True)
    title = "AI-proposed guideline improvements (draft)"
    body = "Automated draft. Review before merge."
    subprocess.run(
        ["gh", "pr", "create", "--title", title, "--body", body],
        cwd=ROOT,
        check=True,
    )
    print("draft PR created")
    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    try:
        sys.exit(main(args.dry_run))
    except Exception as exc:  # noqa: BLE001
        print(f"ai docs draft failed: {exc}", file=sys.stderr)
        sys.exit(0)
