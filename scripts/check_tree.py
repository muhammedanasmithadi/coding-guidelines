"""Fail CI when repo hygiene slips: NULs, empties, version drift, orphaned examples."""

from __future__ import annotations

import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import datetime as dt  # noqa: E402

from check_waivers import find_expired, find_invalid  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKIP_DIRS = {
    ".git",
    ".ruff_cache",
    ".pytest_cache",
    ".mypy_cache",
    "__pycache__",
    "node_modules",
    ".venv",
    "dist",
    "build",
}
SKIP_NAMES = {".coverage", "cover.out", "sbom.json"}
SKIP_SUFFIXES = (".pyc", ".tar.gz", ".tgz", ".zip", ".whl")
TEXT_SUFFIXES = {
    ".md",
    ".yml",
    ".yaml",
    ".json",
    ".toml",
    ".mjs",
    ".py",
    ".sh",
    ".txt",
    ".js",
    ".ts",
    ".cfg",
    ".ini",
}
VERSION_RE = re.compile(r"^## \[([0-9]+\.[0-9]+\.[0-9]+)\]", re.MULTILINE)
EXAMPLES_HEADER_RE = re.compile(r"^## Examples\b", re.MULTILINE)
EXEMPT_DIRS = {"docs/adr"}
COMMENT_SCAN_SUFFIXES = {".py", ".mjs", ".js", ".ts", ".sh", ".yml", ".yaml", ".toml"}
COMMENT_SCAN_NAMES = {"Makefile"}
DIRECTIVE_RE = re.compile(
    r"(#\s*(noqa|pragma|type:|fmt:|isort:|cspell:|!|coding[:=])"
    r"|//\s*eslint-(disable|enable))"
)


def _strip_line_strings(line: str) -> str:
    out = []
    quote: str | None = None
    i = 0
    while i < len(line):
        ch = line[i]
        if quote is None and ch in "\"'":
            quote = ch
        elif quote is not None and ch == quote and line[i - 1] != "\\":
            quote = None
            out.append(" ")
            i += 1
            continue
        if quote is None:
            out.append(ch)
        else:
            out.append(" ")
        i += 1
    return "".join(out)


def _comment_problems_py(path: pathlib.Path, rel: str) -> list[str]:
    import io
    import tokenize

    problems = []
    try:
        tokens = tokenize.generate_tokens(io.StringIO(path.read_text()).readline)
        for tok in tokens:
            if tok.type != tokenize.COMMENT:
                continue
            if DIRECTIVE_RE.search(tok.string):
                continue
            problems.append(f"{rel}:{tok.start[0]}: comment")
    except (OSError, SyntaxError, tokenize.TokenError):
        problems.append(f"{rel}: unparseable")
    return problems


def _comment_problems_lines(path: pathlib.Path, rel: str, marker: str) -> list[str]:
    problems = []
    for n, line in enumerate(path.read_text().splitlines(), 1):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#!") and n == 1:
            continue
        code = _strip_line_strings(line)
        idx = code.find(marker)
        if idx == -1:
            continue
        if code[:idx].strip():
            if marker == "#" or not stripped.startswith("//"):
                if DIRECTIVE_RE.search(line[idx:]):
                    continue
                problems.append(f"{rel}:{n}: comment")
        else:
            if DIRECTIVE_RE.search(stripped):
                continue
            problems.append(f"{rel}:{n}: comment")
    return problems


def check_comments(root: pathlib.Path = ROOT) -> list[str]:
    problems = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        if any(d in rel.parts for d in SKIP_DIRS):
            continue
        if p.name in SKIP_NAMES or str(rel).endswith(SKIP_SUFFIXES):
            continue
        if p.suffix == ".py":
            problems += _comment_problems_py(p, str(rel))
        elif p.suffix in (".mjs", ".js", ".ts"):
            problems += _comment_problems_lines(p, str(rel), "//")
        elif (
            p.suffix in (".sh", ".yml", ".yaml", ".toml")
            or p.name in COMMENT_SCAN_NAMES
        ):
            problems += _comment_problems_lines(p, str(rel), "#")
    return problems


def check_files(root: pathlib.Path = ROOT) -> list[str]:
    problems = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        if any(d in rel.parts for d in SKIP_DIRS):
            continue
        if p.name in SKIP_NAMES or str(rel).endswith(SKIP_SUFFIXES):
            continue
        b = p.read_bytes()
        if b"\x00" in b:
            problems.append(f"{rel}: NUL bytes")
        elif len(b) == 0 and p.suffix in TEXT_SUFFIXES:
            problems.append(f"{rel}: empty")
    return problems


def check_version(root: pathlib.Path = ROOT) -> list[str]:
    problems = []
    version_file = root / "VERSION"
    changelog = root / "CHANGELOG.md"
    package = root / "package.json"
    if not version_file.exists():
        return ["VERSION: missing"]
    if not changelog.exists():
        return ["CHANGELOG.md: missing"]
    version = version_file.read_text().strip()
    match = VERSION_RE.search(changelog.read_text())
    if not match:
        problems.append("CHANGELOG.md: no ## [x.y.z] entry")
    elif match.group(1) != version:
        problems.append(f"VERSION {version} != CHANGELOG {match.group(1)}")
    if package.exists():
        try:
            pkg_version = json.loads(package.read_text()).get("version")
        except ValueError:
            problems.append("package.json: invalid JSON")
        else:
            if pkg_version != version:
                problems.append(f"VERSION {version} != package.json {pkg_version}")
    return problems


def _pool(root: pathlib.Path) -> str:
    parts = []
    for base in ("docs", "checks", "README.md", ".github", "CONTRIBUTING.md"):
        p = root / base
        if p.is_file():
            parts.append(p.read_text())
        elif p.is_dir():
            for f in sorted(p.rglob("*.md")):
                parts.append(f.read_text())
    return "\n".join(parts)


def check_examples_linked(root: pathlib.Path = ROOT) -> list[str]:
    pool = _pool(root)
    orphans = []
    for f in sorted((root / "examples" / "good-vs-bad").glob("*.md")):
        if f.name == "README.md":
            continue
        if f.name not in pool:
            orphans.append(f"examples/good-vs-bad/{f.name}: orphaned")
    return orphans


EXAMPLE_REF_RE = re.compile(
    r"examples/(?:good-vs-bad|minimal|full)/([A-Za-z0-9_.-]+\.(?:md|yaml|yml))"
)


def check_dangling(root: pathlib.Path = ROOT) -> list[str]:
    problems = []
    for base in ("docs", "checks", "README.md", ".github"):
        p = root / base
        files = [p] if p.is_file() else sorted(p.rglob("*.md"))
        for f in files:
            for m in EXAMPLE_REF_RE.finditer(f.read_text()):
                target = root / "examples" / m.group(0).split("examples/", 1)[1]
                if not target.exists():
                    problems.append(f"{f.relative_to(root)}: dangling `{m.group(0)}`")
    return problems


def check_docs_examples(root: pathlib.Path = ROOT) -> list[str]:
    missing = []
    for base in ("docs", "docs/languages"):
        for f in sorted((root / base).glob("*.md")):
            if any(str(f.relative_to(root)).startswith(e) for e in EXEMPT_DIRS):
                continue
            if not EXAMPLES_HEADER_RE.search(f.read_text()):
                missing.append(f"{f.relative_to(root)}: no ## Examples")
    return missing


def check_waivers(root: pathlib.Path = ROOT) -> list[str]:
    path = root / "waivers" / "active.yml"
    today = dt.date.today()
    try:
        expired = find_expired(path, today)
        invalid = find_invalid(path, today)
    except (OSError, ValueError) as e:
        return [f"waivers/active.yml: unreadable ({e})"]
    problems = [f"waivers: {e}" for e in expired]
    problems += [f"waivers: {e}" for e in invalid]
    return problems


def main(root: pathlib.Path = ROOT) -> int:
    problems = (
        check_files(root)
        + check_version(root)
        + check_examples_linked(root)
        + check_dangling(root)
        + check_docs_examples(root)
        + check_comments(root)
        + check_waivers(root)
    )
    if problems:
        print("\n".join(problems))
        return 1
    print("tree ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
