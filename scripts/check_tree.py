from __future__ import annotations

import ast
import json
import pathlib
import re
import sys
from typing import TypedDict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import datetime as dt  # noqa: E402

import yaml  # noqa: E402
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
    ".hypothesis",
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
ADR_DIR = "docs/adr"
ADR_FILE_RE = re.compile(r"^(\d{4})-[a-z0-9-]+\.md$")
ADR_TITLE_RE = re.compile(r"^# ADR (\d{4}): (.+)$", re.MULTILINE)
ADR_REF_RE = re.compile(r"ADR[- ](\d{4})|adr/(\d{4})")
ADR_FIELDS = ("Status", "Context", "Options", "Decision", "Consequences", "Enforcement")
ADR_STATUSES = ("proposed", "accepted", "superseded")
ADR_TEMPLATE = "0001-template.md"
BLOCK_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
BLOCK_DIRECTIVE_RE = re.compile(
    r"(?:eslint|oxlint)-(?:disable|enable)"
    r"|(?:istanbul|v8|c8)\s*ignore"
    r"|prettier-ignore"
)


class _AdrEntry(TypedDict):
    num: str
    path: pathlib.Path
    rel: pathlib.Path
    text: str
    status: str | None
    supersedes: str | None
    enforcement: str | None


COMMENT_SCAN_SUFFIXES = {".py", ".mjs", ".js", ".ts", ".sh", ".yml", ".yaml", ".toml"}
COMMENT_SCAN_NAMES = {"Makefile"}
DIRECTIVE_RE = re.compile(
    r"(#\s*(noqa|pragma|type:|fmt:|isort:|cspell:|!|coding[:=])"
    r"|//\s*eslint-(disable|enable)"
    r"|//\s*oxlint-disable(?:-next-line|-line)?"
    r"|(?://|/\*+)\s*(?:istanbul|v8|c8)\s+ignore"
    r"|//\s*prettier-ignore"
    r"|#\s*(?:pragma|coverage):\s*(?:no|nocover)\b)"
)


SHELL_PARAM_HASH_RE = re.compile(r"\$\{[^}]*#[^}]*\}")


def _strip_line_strings(line: str) -> str:
    line = SHELL_PARAM_HASH_RE.sub(lambda m: " " * len(m.group(0)), line)
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
    except OSError, SyntaxError, tokenize.TokenError:
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


def _comment_problems_blocks(path: pathlib.Path, rel: str) -> list[str]:
    problems = []
    try:
        text = path.read_text()
    except OSError:
        return [f"{rel}: unreadable"]
    stripped = "".join(
        _strip_line_strings(line) for line in text.splitlines(keepends=True)
    )
    for m in BLOCK_COMMENT_RE.finditer(stripped):
        if BLOCK_DIRECTIVE_RE.search(m.group(0)):
            continue
        line = stripped.count("\n", 0, m.start()) + 1
        problems.append(f"{rel}:{line}: comment")
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
            problems += _comment_problems_blocks(p, str(rel))
        elif (
            p.suffix in (".sh", ".yml", ".yaml", ".toml")
            or p.name in COMMENT_SCAN_NAMES
        ):
            problems += _comment_problems_lines(p, str(rel), "#")
    return problems


def check_docstrings(root: pathlib.Path = ROOT) -> list[str]:
    problems = []
    for p in sorted(root.rglob("*.py")):
        rel = p.relative_to(root)
        if any(d in rel.parts for d in SKIP_DIRS) or p.name in SKIP_NAMES:
            continue
        try:
            tree = ast.parse(p.read_text())
        except OSError, SyntaxError:
            continue
        docstring_lines = set()
        for node in ast.walk(tree):
            if not isinstance(
                node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
            ):
                continue
            if ast.get_docstring(node) is None:
                continue
            line = node.body[0].lineno
            docstring_lines.add(line)
            problems.append(f"{rel}:{line}: docstring")
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Expr)
                and isinstance(node.value, ast.Constant)
                and isinstance(node.value.value, str)
                and node.lineno not in docstring_lines
            ):
                problems.append(f"{rel}:{node.lineno}: string literal statement")
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
        if p.name.startswith("baseline."):
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


SOURCES_RE = re.compile(r"^\s*sources?:", re.MULTILINE | re.IGNORECASE)


def check_sources(root: pathlib.Path = ROOT) -> list[str]:
    missing = []
    for base in ("docs", "docs/languages"):
        for f in sorted((root / base).glob("*.md")):
            if any(str(f.relative_to(root)).startswith(e) for e in EXEMPT_DIRS):
                continue
            if not SOURCES_RE.search(f.read_text()):
                missing.append(f"{f.relative_to(root)}: no Sources")
    return missing


check_docs_sources = check_sources


def check_waivers(root: pathlib.Path = ROOT) -> list[str]:
    path = root / "waivers" / "active.yml"
    today = dt.datetime.now(dt.UTC).date()
    try:
        expired = find_expired(path, today)
        invalid = find_invalid(path, today)
    except (OSError, ValueError) as e:
        return [f"waivers/active.yml: unreadable ({e})"]
    problems = [f"waivers: {e}" for e in expired]
    problems += [f"waivers: {e}" for e in invalid]
    return problems


def _adr_files(root: pathlib.Path) -> list[pathlib.Path]:
    d = root / ADR_DIR
    if not d.is_dir():
        return []
    return sorted(p for p in d.glob("*.md") if ADR_FILE_RE.match(p.name))


def _adr_field(text: str, name: str) -> str | None:
    m = re.search(rf"^- {name}: *(.*)$", text, re.MULTILINE)
    if not m:
        return None
    return m.group(1).strip()


def _adr_num(name: str) -> str:
    m = ADR_FILE_RE.match(name)
    return m.group(1) if m else ""


def _adr_entries(root: pathlib.Path) -> list[_AdrEntry]:
    entries: list[_AdrEntry] = []
    for p in _adr_files(root):
        text = p.read_text()
        entries.append(
            {
                "num": _adr_num(p.name),
                "path": p,
                "rel": p.relative_to(root),
                "text": text,
                "status": _adr_field(text, "Status"),
                "supersedes": _adr_field(text, "Supersedes"),
                "enforcement": _adr_field(text, "Enforcement"),
            }
        )
    return entries


def _adr_title_problems(entry: _AdrEntry) -> list[str]:
    title = ADR_TITLE_RE.search(entry["text"])
    if not title:
        return [f"{entry['rel']}: missing '# ADR NNNN: title' heading"]
    if title.group(1) != entry["num"]:
        return [
            f"{entry['rel']}: title number {title.group(1)} != filename {entry['num']}"
        ]
    return []


def _adr_fields_problems(entry: _AdrEntry) -> list[str]:
    rel = entry["rel"]
    problems = []
    for field in ADR_FIELDS:
        value = _adr_field(entry["text"], field)
        if value is None:
            problems.append(f"{rel}: missing '{field}' field")
        elif field != "Status" and not value:
            problems.append(f"{rel}: empty '{field}' field")
    status = entry["status"]
    if status is not None and status not in ADR_STATUSES:
        problems.append(f"{rel}: status '{status}' not in {ADR_STATUSES}")
    sup = entry["supersedes"]
    if sup and not re.search(r"(\d{4})", sup):
        problems.append(f"{rel}: bad Supersedes value '{sup}'")
    return problems


def _adr_file_problems(entry: _AdrEntry) -> list[str]:
    rel = entry["rel"]
    text = entry["text"]
    if entry["path"].name == ADR_TEMPLATE:
        return [
            f"{rel}: template missing '{field}' field"
            for field in ADR_FIELDS
            if not re.search(rf"^- {field}:", text, re.MULTILINE)
        ]
    return _adr_title_problems(entry) + _adr_fields_problems(entry)


def _adr_chain_problems(entries: list[_AdrEntry]) -> list[str]:
    by_num = {e["num"]: e for e in entries}
    problems = []
    superseded_by = {}
    for e in entries:
        sup = e["supersedes"]
        if not sup:
            continue
        m = re.search(r"(\d{4})", sup)
        if not m:
            continue
        target = m.group(1)
        superseded_by[target] = e["num"]
        if target not in by_num:
            problems.append(f"{e['rel']}: supersedes missing ADR-{target}")
            continue
        if by_num[target]["status"] != "superseded":
            problems.append(
                f"{e['rel']}: ADR-{target} is '{by_num[target]['status']}',"
                " expected superseded"
            )
        if int(target) >= int(e["num"]):
            problems.append(f"{e['rel']}: supersedes ADR-{target}, which is not older")
    for e in entries:
        if e["status"] == "superseded" and e["num"] not in superseded_by:
            problems.append(f"{ADR_DIR}/{e['path'].name}: superseded by no ADR")
    return problems


ARTIFACT_SUFFIXES = (".py", ".sh", ".yml", ".yaml", ".json", ".md", ".toml")
ENFORCEMENT_TOKEN_RE = re.compile(r"`([^`]+)`")


def _defines_function(root: pathlib.Path, script: str, name: str) -> bool:
    path = root / script
    if not path.exists():
        return True
    try:
        text = path.read_text()
    except OSError:
        return True
    return f"def {name}(" in text


def _adr_enforcement_problems(root: pathlib.Path, entry: _AdrEntry) -> list[str]:
    value = entry["enforcement"] or ""
    if not value or "review" in value.lower():
        return []
    problems: list[str] = []
    script = "scripts/check_tree.py"
    for token in ENFORCEMENT_TOKEN_RE.findall(value):
        if token.endswith(ARTIFACT_SUFFIXES):
            if not (root / token).exists():
                problems.append(f"{entry['rel']}: Enforcement names missing {token}")
            if token.startswith("scripts/"):
                script = token
        elif token.startswith("check_") and not _defines_function(root, script, token):
            problems.append(
                f"{entry['rel']}: Enforcement names missing {token} in {script}"
            )
    return problems


ADR_INDEX_ROW_RE = re.compile(r"^\|\s*(\d{4})\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|$")


def _adr_index_problems(root: pathlib.Path, entries: list[_AdrEntry]) -> list[str]:
    index = root / ADR_DIR / "README.md"
    if not index.exists():
        return []
    rows: dict[str, tuple[str, str]] = {}
    for line in index.read_text().splitlines():
        m = ADR_INDEX_ROW_RE.match(line.strip())
        if m:
            rows[m.group(1)] = (m.group(2), m.group(3))
    superseders: dict[str, str] = {}
    for e in entries:
        sup = e["supersedes"]
        if not sup:
            continue
        m = re.search(r"(\d{4})", sup)
        if m:
            superseders[m.group(1)] = e["num"]
    problems: list[str] = []
    known = {e["num"] for e in entries}
    for e in entries:
        problems += _adr_index_row_problems(e, rows, superseders)
    for num in rows:
        if num not in known:
            problems.append(
                f"{ADR_DIR}/README.md: lists ADR-{num}, which does not exist"
            )
    return problems


def _adr_index_row_problems(
    entry: _AdrEntry,
    rows: dict[str, tuple[str, str]],
    superseders: dict[str, str],
) -> list[str]:
    num = entry["num"]
    if num not in rows:
        return [f"{ADR_DIR}/README.md: ADR-{num} is not listed"]
    title, status = rows[num]
    heading = ADR_TITLE_RE.search(entry["text"])
    expected_title = heading.group(2).strip() if heading else ""
    expected_status = entry["status"] or ""
    if num in superseders:
        expected_status = f"superseded by {superseders[num]}"
    problems = []
    if title != expected_title:
        problems.append(
            f"{ADR_DIR}/README.md: ADR-{num} title '{title}' != '{expected_title}'"
        )
    if status != expected_status:
        problems.append(
            f"{ADR_DIR}/README.md: ADR-{num} status '{status}' != '{expected_status}'"
        )
    return problems


def check_adr_records(root: pathlib.Path = ROOT) -> list[str]:
    entries = _adr_entries(root)
    if not entries:
        return []
    problems = []
    for e in entries:
        problems += _adr_file_problems(e)
        problems += _adr_enforcement_problems(root, e)
    problems += _adr_chain_problems(entries)
    problems += _adr_index_problems(root, entries)
    ordered = sorted(int(e["num"]) for e in entries)
    if ordered and ordered != list(range(1, max(ordered) + 1)):
        problems.append(f"{ADR_DIR}: numbering is not sequential")
    return problems


def _live_docs(root: pathlib.Path) -> list[pathlib.Path]:
    files = []
    for base in ("docs", "checks", "examples"):
        p = root / base
        if not p.is_dir():
            continue
        for f in sorted(p.rglob("*.md")):
            rel = f.relative_to(root)
            if rel.parts[:2] == ("docs", "adr"):
                continue
            files.append(f)
    for base in ("README.md", "CONTRIBUTING.md"):
        p = root / base
        if p.is_file():
            files.append(p)
    p = root / ".github"
    if p.is_dir():
        files.extend(sorted(p.rglob("*.md")))
    return files


def check_adr_links(root: pathlib.Path = ROOT) -> list[str]:
    problems: list[str] = []
    adr_dir = root / ADR_DIR
    if not adr_dir.is_dir():
        return problems
    existing = {
        _adr_num(p.name) for p in adr_dir.glob("*.md") if ADR_FILE_RE.match(p.name)
    }
    referenced = set()
    for f in _live_docs(root):
        rel = f.relative_to(root)
        for m in ADR_REF_RE.finditer(f.read_text()):
            num = m.group(1) or m.group(2)
            if num not in existing:
                problems.append(f"{rel}: dangling ADR-{num}")
            else:
                referenced.add(num)
    for p in sorted(adr_dir.glob("*.md")):
        num = _adr_num(p.name)
        if not num or _adr_field(p.read_text(), "Status") != "accepted":
            continue
        if num not in referenced:
            problems.append(f"{ADR_DIR}/{p.name}: accepted ADR referenced by no doc")
    return problems


ENFORCE_REF_RE = re.compile(r"enforce/[A-Za-z0-9._/-]+")


def check_language_configs(root: pathlib.Path = ROOT) -> list[str]:
    problems: list[str] = []
    lang_dir = root / "docs" / "languages"
    if not lang_dir.is_dir():
        return problems
    for doc in sorted(lang_dir.glob("*.md")):
        rel = doc.relative_to(root)
        if doc.stem == "core":
            continue
        enforce_dir = root / "enforce" / doc.stem
        if not enforce_dir.is_dir() or not any(
            p.is_file() for p in enforce_dir.iterdir()
        ):
            problems.append(f"{rel}: no enforce/{doc.stem} config")
    return problems


def check_enforce_refs(root: pathlib.Path = ROOT) -> list[str]:
    problems: list[str] = []
    for f in _live_docs(root):
        rel = f.relative_to(root)
        for m in ENFORCE_REF_RE.finditer(f.read_text()):
            target = root / m.group(0).rstrip(".")
            if not target.exists():
                problems.append(f"{rel}: dangling `{m.group(0)}`")
    return problems


DEPRECATED_ENDPOINT_RE = re.compile(r"/healthz")


def check_health_endpoints(root: pathlib.Path = ROOT) -> list[str]:
    problems: list[str] = []
    for f in _live_docs(root):
        rel = f.relative_to(root)
        for n, line in enumerate(f.read_text().splitlines(), 1):
            if not DEPRECATED_ENDPOINT_RE.search(line):
                continue
            if "deprecated" in line.lower():
                continue
            problems.append(
                f"{rel}:{n}: deprecated /healthz, use /livez + /readyz (ADR-0002)"
            )
    return problems


RUNTIME_BASELINE = "enforce/runtime-baseline.yml"
RUNTIME_PINS = (("python", ".python-version"), ("node", ".nvmrc"))


def _adr_accepted(root: pathlib.Path, num: str) -> bool:
    for p in _adr_files(root):
        if _adr_num(p.name) == num:
            return _adr_field(p.read_text(), "Status") == "accepted"
    return False


def _runtime_adr_problems(
    root: pathlib.Path, runtime: str, entry: dict[str, object]
) -> list[str]:
    rationale = entry.get("rationale")
    if not rationale:
        return [f"{RUNTIME_BASELINE}: {runtime} needs a 'rationale' ADR id"]
    m = re.search(r"(\d{4})", str(rationale))
    if not m:
        return [
            f"{RUNTIME_BASELINE}: {runtime} rationale '{rationale}' is not an ADR id"
        ]
    if not _adr_accepted(root, m.group(1)):
        return [
            f"{RUNTIME_BASELINE}: {runtime} rationale {rationale}"
            " is not an accepted ADR"
        ]
    return []


def _runtime_pin_problems(
    root: pathlib.Path, entry: dict[str, object], pin_name: str
) -> list[str]:
    pin = root / pin_name
    if not pin.exists():
        return [f"{pin_name}: missing"]
    value = pin.read_text().strip()
    series = str(entry["series"])
    if not value.startswith(f"{series}."):
        return [
            f"{pin_name}: {value} is outside series {series}; a major move updates "
            f"{RUNTIME_BASELINE} in the same PR as its ADR (ADR-0007)"
        ]
    return []


def check_runtime_baseline(root: pathlib.Path = ROOT) -> list[str]:
    path = root / RUNTIME_BASELINE
    if not path.exists():
        return []
    try:
        data = yaml.safe_load(path.read_text())
    except yaml.YAMLError as e:
        return [f"{RUNTIME_BASELINE}: invalid YAML ({e})"]
    if not isinstance(data, dict):
        return [f"{RUNTIME_BASELINE}: top level must be a mapping"]
    problems: list[str] = []
    for runtime, pin_name in RUNTIME_PINS:
        entry = data.get(runtime)
        if not isinstance(entry, dict) or not entry.get("series"):
            problems.append(f"{RUNTIME_BASELINE}: missing '{runtime}.series'")
            continue
        problems += _runtime_adr_problems(root, runtime, entry)
        problems += _runtime_pin_problems(root, entry, pin_name)
    return problems


def check_waiver_adr_links(root: pathlib.Path = ROOT) -> list[str]:
    path = root / "waivers" / "active.yml"
    if not path.exists():
        return []
    try:
        entries = yaml.safe_load(path.read_text()) or []
    except yaml.YAMLError as e:
        return [f"waivers/active.yml: invalid YAML ({e})"]
    if not isinstance(entries, list):
        return []
    existing = {_adr_num(p.name) for p in _adr_files(root) if ADR_FILE_RE.match(p.name)}
    problems: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        rationale = entry.get("adr")
        if not rationale:
            continue
        m = re.search(r"(\d{4})", str(rationale))
        if not m or m.group(1) not in existing:
            problems.append(
                f"waivers/active.yml: {entry.get('id', '?')} cites unknown {rationale}"
            )
    return problems


BASELINE_PATH = "waivers/baseline.check-tree.json"


def collect_problems(root: pathlib.Path) -> list[str]:
    return (
        check_files(root)
        + check_version(root)
        + check_examples_linked(root)
        + check_dangling(root)
        + check_docs_examples(root)
        + check_sources(root)
        + check_comments(root)
        + check_docstrings(root)
        + check_adr_records(root)
        + check_adr_links(root)
        + check_language_configs(root)
        + check_enforce_refs(root)
        + check_health_endpoints(root)
        + check_runtime_baseline(root)
        + check_waiver_adr_links(root)
        + check_waivers(root)
    )


def load_baseline(root: pathlib.Path) -> set[str]:
    path = root / BASELINE_PATH
    if not path.exists():
        return set()
    try:
        data = json.loads(path.read_text())
    except (OSError, ValueError) as e:
        print(f"{BASELINE_PATH}: unreadable ({e})", file=sys.stderr)
        return set()
    if not isinstance(data, list):
        print(f"{BASELINE_PATH}: top level must be a list", file=sys.stderr)
        return set()
    return {str(item) for item in data}


def main(root: pathlib.Path = ROOT, as_json: bool = False) -> int:
    problems = collect_problems(root)
    baseline = load_baseline(root)
    fresh = [p for p in problems if p not in baseline]
    if as_json:
        print(json.dumps(sorted(problems), indent=2))
        return 1 if fresh else 0
    for p in fresh:
        print(p)
    for p in sorted(baseline & set(problems)):
        print(f"baseline: {p}")
    for p in sorted(baseline - set(problems)):
        print(f"stale baseline entry: {p}")
    if fresh:
        return 1
    if baseline:
        print(f"tree ok ({len(baseline)} baselined findings)")
        return 0
    print("tree ok")
    return 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = pathlib.Path(args[0]) if args else ROOT
    sys.exit(main(root, as_json="--format=json" in sys.argv))
