from __future__ import annotations

import datetime as dt
import json
import pathlib
import re
import subprocess
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

from check_tree import (  # noqa: E402
    check_adr_links,
    check_adr_records,
    check_dangling,
    check_docs_examples,
    check_docstrings,
    check_enforce_refs,
    check_examples_linked,
    check_files,
    check_health_endpoints,
    check_language_configs,
    check_runtime_baseline,
    check_version,
    check_waivers,
    main,
)


def write_waivers(root: pathlib.Path, entries: list[dict]) -> None:
    wdir = root / "waivers"
    wdir.mkdir(parents=True, exist_ok=True)
    (wdir / "active.yml").write_text(yaml.safe_dump(entries))


def adr_body(
    num: str,
    title: str,
    status: str = "accepted",
    options: str = "(A) keep, (B) change",
    supersedes: str | None = None,
) -> str:
    lines = [
        f"# ADR {num}: {title}",
        "",
        f"- Status: {status}",
        "- Context: context",
        f"- Options: {options}",
        "- Decision: decision",
        "- Consequences: consequences",
        "- Enforcement: review",
    ]
    if supersedes:
        lines.append(f"- Supersedes: {supersedes}")
    return "\n".join(lines) + "\n"


def write_adr(root: pathlib.Path, num: str, slug: str, body: str) -> pathlib.Path:
    d = root / "docs" / "adr"
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{num}-{slug}.md"
    p.write_text(body)
    write_adr_index(root)
    return p


def write_adr_index(root: pathlib.Path) -> None:
    d = root / "docs" / "adr"
    if not d.is_dir():
        return
    records = {}
    superseders = {}
    for p in sorted(d.glob("*.md")):
        if not re.match(r"^\d{4}-", p.name) or p.name == "0001-template.md":
            continue
        text = p.read_text()
        title = re.search(r"^# ADR \d{4}: (.+)$", text, re.MULTILINE)
        status = re.search(r"^- Status: *(.*)$", text, re.MULTILINE)
        sup = re.search(r"^- Supersedes: *ADR-(\d{4})", text, re.MULTILINE)
        if not title or not status:
            continue
        records[p.name[:4]] = (title.group(1), status.group(1))
        if sup:
            superseders[sup.group(1)] = p.name[:4]
    rows = []
    for num, (title, status) in records.items():
        if num in superseders:
            status = f"superseded by {superseders[num]}"
        rows.append(f"| {num} | {title} | {status} |")
    index = d / "README.md"
    if rows:
        index.write_text(
            "| ADR | Title | Status |\n|---|---|---|\n" + "\n".join(rows) + "\n"
        )
    elif index.exists():
        index.unlink()


def make_tree(tmp: pathlib.Path) -> pathlib.Path:
    (tmp / "docs" / "languages").mkdir(parents=True)
    (tmp / "checks").mkdir()
    (tmp / "examples" / "good-vs-bad").mkdir(parents=True)
    (tmp / "enforce" / "b").mkdir(parents=True)
    (tmp / "enforce" / "b" / "conf.yml").write_text("x: 1\n")
    (tmp / "VERSION").write_text("0.6.0\n")
    (tmp / "CHANGELOG.md").write_text("## [0.6.0] - 2026-10-10\n")
    (tmp / "package.json").write_text('{"version": "0.6.0"}\n')
    (tmp / "docs" / "a.md").write_text("# A\n\nSources: x\n\n## Examples\n- e.md\n")
    (tmp / "docs" / "languages" / "b.md").write_text(
        "# B\n\nSources: y\n\n## Examples\n- y\n"
    )
    (tmp / "examples" / "good-vs-bad" / "e.md").write_text("# E\n")
    future = (dt.datetime.now(dt.UTC).date() + dt.timedelta(days=10)).isoformat()
    write_waivers(
        tmp,
        [
            {
                "id": "W1",
                "rule": "r",
                "reason": "t",
                "owner": "@t",
                "expires": future,
                "issue": "https://example.com/1",
            }
        ],
    )
    return tmp


def test_clean_tree_ok(tmp_path: pathlib.Path) -> None:
    assert main(make_tree(tmp_path)) == 0


def test_nul_empty_and_version_problems(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / "docs" / "empty.md").write_text("")
    (root / "docs" / "nul.md").write_bytes(b"a\x00b")
    (root / "VERSION").write_text("9.9.9\n")
    assert any("empty" in p for p in check_files(root))
    assert any("NUL" in p for p in check_files(root))
    assert check_version(root) != []
    assert main(root) == 1


def test_generated_artifacts_skipped(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / ".coverage").write_bytes(b"\x00sqlite")
    (root / "node_modules" / "pkg").mkdir(parents=True)
    (root / "node_modules" / "pkg" / "b.node").write_bytes(b"\x00bin")
    assert check_files(root) == []


def test_archives_skipped(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / "bundle.tar.gz").write_bytes(b"\x00data")
    assert check_files(root) == []


def test_stem_substring_does_not_satisfy_link(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / "examples" / "good-vs-bad" / "orphan.md").write_text("# O\n")
    (root / "docs" / "a.md").write_text("# A\n\n## Examples\norphans everywhere\n")
    orphans = check_examples_linked(root)
    assert "examples/good-vs-bad/orphan.md: orphaned" in orphans
    assert "examples/good-vs-bad/e.md: orphaned" in orphans
    (root / "docs" / "a.md").write_text("# A\n\n## Examples\n- e.md\n- orphan.md\n")
    assert check_examples_linked(root) == []


def test_hash_header_does_not_count(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / "docs" / "bare.md").write_text("# bare\n\n### Examples\n- e.md\n")
    assert check_docs_examples(root) == ["docs/bare.md: no ## Examples"]


def test_dangling_reference(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / "docs" / "a.md").write_text(
        "# A\n\n## Examples\n- examples/good-vs-bad/ghost.md\n- e.md\n"
    )
    dangling = "docs/a.md: dangling `examples/good-vs-bad/ghost.md`"
    assert check_dangling(root) == [dangling]


def test_package_version_enforced(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / "package.json").write_text('{"version": "0.0.1"}\n')
    assert any("package.json" in p for p in check_version(root))


def test_bad_waivers_fail(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    past = (dt.datetime.now(dt.UTC).date() - dt.timedelta(days=1)).isoformat()
    write_waivers(
        tmp_path,
        [
            {
                "id": "W2",
                "rule": "r",
                "reason": "t",
                "owner": "@t",
                "expires": past,
                "issue": "https://example.com/2",
            }
        ],
    )
    assert check_waivers(root) != []
    (root / "waivers" / "active.yml").write_text("::: not yaml [[[\n- {id: x}\n")
    assert check_waivers(root) != []


def test_baseline_artifacts_skipped(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    wdir = root / "waivers"
    wdir.mkdir(parents=True, exist_ok=True)
    (wdir / "baseline.ruff.json").write_bytes(b"\x00bad")
    assert check_files(root) == []


def test_oxlint_directive_allowed(tmp_path: pathlib.Path) -> None:
    from check_tree import check_comments

    root = make_tree(tmp_path)
    (root / "w.mjs").write_text(
        "const u = 1;\n// oxlint-disable-next-line no-console\n"
    )
    problems = check_comments(root)
    assert not [p for p in problems if "w.mjs:2" in p]


def test_comments_banned_except_directives(tmp_path: pathlib.Path) -> None:
    from check_tree import check_comments

    root = make_tree(tmp_path)
    (root / "x.py").write_text("import os  # noqa: F401\n# explain\n")
    (root / "y.sh").write_text("#!/usr/bin/env bash\n# usage note\n")
    (root / "z.yaml").write_text("a: 1  # trailing\n")
    (root / "w.mjs").write_text('const u = "https://x.y/z";\n// narrate\n')
    problems = check_comments(root)
    assert "x.py:2: comment" in problems
    assert "y.sh:2: comment" in problems
    assert "z.yaml:1: comment" in problems
    assert "w.mjs:2: comment" in problems
    assert not [p for p in problems if "x.py:1" in p]


def test_missing_source_fails(tmp_path: pathlib.Path) -> None:
    from check_tree import check_sources

    root = make_tree(tmp_path)
    (root / "docs" / "a.md").write_text("# A\n\n## Examples\n- e.md\n")
    assert any("no Sources" in p for p in check_sources(root))


def test_cli_root_override(tmp_path: pathlib.Path) -> None:
    import subprocess

    root = make_tree(tmp_path)
    script = pathlib.Path(__file__).resolve().parents[1]
    script = script / "scripts" / "check_tree.py"
    proc = subprocess.run(
        [sys.executable, str(script), str(root)], capture_output=True, text=True
    )
    assert proc.returncode == 0, proc.stdout


def test_docstrings_banned(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / "m.py").write_text('"""Module purpose."""\n\nimport os\n')
    problems = check_docstrings(root)
    assert any("docstring" in p for p in problems)


def test_bare_string_statement_banned(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / "m.py").write_text('import os\n\n"a note"\n')
    problems = check_docstrings(root)
    assert any("string literal statement" in p for p in problems)


def test_clean_python_has_no_docstring_problem(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / "m.py").write_text("import os\n\n\ndef f() -> int:\n    return 1\n")
    assert check_docstrings(root) == []


def test_block_comment_banned(tmp_path: pathlib.Path) -> None:
    from check_tree import check_comments

    root = make_tree(tmp_path)
    (root / "a.ts").write_text("const x = 1;\n/* explain */\n")
    problems = check_comments(root)
    assert any("a.ts:2: comment" in p for p in problems)


def test_block_directive_allowed(tmp_path: pathlib.Path) -> None:
    from check_tree import check_comments

    root = make_tree(tmp_path)
    (root / "a.ts").write_text("const x = 1;\n/* eslint-disable no-console */\n")
    problems = check_comments(root)
    assert not [p for p in problems if "a.ts:2" in p]


def test_shell_parameter_expansion_is_not_a_comment(tmp_path: pathlib.Path) -> None:
    from check_tree import check_comments

    root = make_tree(tmp_path)
    (root / "s.sh").write_text('#!/usr/bin/env bash\nn=${#list[@]}\necho "$n"\n')
    problems = check_comments(root)
    assert not [p for p in problems if "s.sh:2" in p]


def test_adr_missing_field_fails(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    write_adr(
        root,
        "0001",
        "one",
        "# ADR 0001: One\n\n- Status: accepted\n- Context: c\n- Decision: d\n",
    )
    problems = check_adr_records(root)
    assert any("missing 'Options' field" in p for p in problems)
    assert any("missing 'Consequences' field" in p for p in problems)


def test_adr_bad_status_fails(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    write_adr(root, "0001", "one", adr_body("0001", "One", status="accepted (pilot)"))
    problems = check_adr_records(root)
    assert any("not in" in p for p in problems)


def test_adr_title_number_must_match_filename(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    write_adr(root, "0001", "one", adr_body("0002", "One"))
    problems = check_adr_records(root)
    assert any("title number 0002 != filename 0001" in p for p in problems)


def test_adr_supersede_chain_ok(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    write_adr(root, "0001", "one", adr_body("0001", "One"))
    write_adr(root, "0002", "two", adr_body("0002", "Two", status="superseded"))
    write_adr(root, "0003", "three", adr_body("0003", "Three", supersedes="ADR-0002"))
    assert check_adr_records(root) == []


def test_adr_superseded_without_successor_fails(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    write_adr(root, "0001", "one", adr_body("0001", "One"))
    write_adr(root, "0002", "two", adr_body("0002", "Two", status="superseded"))
    problems = check_adr_records(root)
    assert any("superseded by no ADR" in p for p in problems)


def test_adr_supersedes_missing_target_fails(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    write_adr(root, "0001", "one", adr_body("0001", "One", supersedes="ADR-0009"))
    problems = check_adr_records(root)
    assert any("supersedes missing ADR-0009" in p for p in problems)


def test_adr_numbering_must_be_sequential(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    write_adr(root, "0001", "one", adr_body("0001", "One"))
    write_adr(root, "0003", "three", adr_body("0003", "Three"))
    problems = check_adr_records(root)
    assert any("numbering is not sequential" in p for p in problems)


def test_adr_dangling_reference_fails(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    write_adr(root, "0001", "one", adr_body("0001", "One"))
    (root / "docs" / "a.md").write_text(
        "# A\n\nSources: x\n\n## Examples\n- e.md\n\nSee ADR-0009.\n"
    )
    problems = check_adr_links(root)
    assert any("dangling ADR-0009" in p for p in problems)


def test_accepted_adr_must_be_referenced(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    write_adr(root, "0001", "one", adr_body("0001", "One"))
    problems = check_adr_links(root)
    assert any("accepted ADR referenced by no doc" in p for p in problems)


def test_referenced_adr_passes(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    write_adr(root, "0001", "one", adr_body("0001", "One"))
    (root / "docs" / "a.md").write_text(
        "# A\n\nSources: x\n\n## Examples\n- e.md\n\nSee ADR-0001.\n"
    )
    assert check_adr_links(root) == []


def test_language_config_required(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / "enforce" / "b" / "conf.yml").unlink()
    problems = check_language_configs(root)
    assert any("no enforce/b config" in p for p in problems)


def test_language_config_reference_must_exist(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / "docs" / "languages" / "b.md").write_text(
        "# B\n\nSources: y\n\n## Examples\n- y\n\n- uses `enforce/b/missing.yml`\n"
    )
    problems = check_enforce_refs(root)
    assert any("dangling `enforce/b/missing.yml`" in p for p in problems)


def test_deprecated_health_endpoint_fails(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / "docs" / "a.md").write_text(
        "# A\n\nSources: x\n\n## Examples\n- e.md\n\n- probe `GET /healthz`\n"
    )
    problems = check_health_endpoints(root)
    assert any("deprecated /healthz" in p for p in problems)


def test_deprecated_endpoint_allowed_in_deprecation_note(
    tmp_path: pathlib.Path,
) -> None:
    root = make_tree(tmp_path)
    (root / "docs" / "a.md").write_text(
        "# A\n\nSources: x\n\n## Examples\n- e.md\n"
        "\n- upstream `healthz` is deprecated\n"
    )
    assert check_health_endpoints(root) == []


def test_enforce_reference_must_exist(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / "docs" / "a.md").write_text(
        "# A\n\nSources: x\n\n## Examples\n- e.md\n\n- `enforce/ghost/config.yml`\n"
    )
    problems = check_enforce_refs(root)
    assert any("dangling `enforce/ghost/config.yml`" in p for p in problems)


def test_runtime_baseline_mismatch_fails(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / "runtime-baseline.yml").write_text(
        'python:\n  series: "3.14"\n  rationale: ADR-0001\n'
        'node:\n  series: "24"\n  rationale: ADR-0001\n'
    )
    (root / ".python-version").write_text("3.15.0\n")
    (root / ".nvmrc").write_text("24.1.0\n")
    problems = check_runtime_baseline(root)
    assert any(".python-version: 3.15.0 is outside series 3.14" in p for p in problems)
    assert not [p for p in problems if ".nvmrc" in p]


def test_runtime_baseline_needs_a_series_per_pinned_runtime(
    tmp_path: pathlib.Path,
) -> None:
    root = make_tree(tmp_path)
    (root / "runtime-baseline.yml").write_text(
        'python:\n  series: "3.14"\n  rationale: ADR-0001\n'
        "node:\n  rationale: ADR-0001\n"
    )
    (root / ".python-version").write_text("3.14.1\n")
    (root / ".nvmrc").write_text("24.1.0\n")
    problems = check_runtime_baseline(root)
    assert any("missing 'node.series'" in p for p in problems)


def test_runtime_baseline_rationale_must_be_accepted(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    write_adr(root, "0001", "one", adr_body("0001", "One", status="superseded"))
    (root / "runtime-baseline.yml").write_text(
        'python:\n  series: "3.14"\n  rationale: ADR-0001\n'
    )
    (root / ".python-version").write_text("3.14.1\n")
    problems = check_runtime_baseline(root)
    assert any("rationale ADR-0001 is not an accepted ADR" in p for p in problems)


def test_runtime_baseline_ignored_when_no_runtime_is_pinned(
    tmp_path: pathlib.Path,
) -> None:
    root = make_tree(tmp_path)
    (root / "runtime-baseline.yml").write_text(
        'python:\n  series: "3.14"\n  rationale: ADR-0001\n'
    )
    assert check_runtime_baseline(root) == []


def test_runtime_baseline_required_when_a_runtime_is_pinned(
    tmp_path: pathlib.Path,
) -> None:
    root = make_tree(tmp_path)
    (root / ".python-version").write_text("3.14.1\n")
    problems = check_runtime_baseline(root)
    assert any("runtime-baseline.yml: missing" in p for p in problems)


def test_adr_requires_enforcement_field(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    write_adr(
        root,
        "0001",
        "one",
        "# ADR 0001: One\n\n- Status: accepted\n- Context: c\n- Options: o\n"
        "- Decision: d\n- Consequences: c\n",
    )
    problems = check_adr_records(root)
    assert any("missing 'Enforcement' field" in p for p in problems)


def test_waiver_must_cite_an_existing_adr(tmp_path: pathlib.Path) -> None:
    from check_tree import check_waiver_adr_links

    root = make_tree(tmp_path)
    write_adr(root, "0001", "one", adr_body("0001", "One"))
    write_waivers(
        root,
        [
            {
                "id": "W3",
                "rule": "r",
                "reason": "t",
                "owner": "@t",
                "expires": (
                    dt.datetime.now(dt.UTC).date() + dt.timedelta(days=5)
                ).isoformat(),
                "issue": "https://example.com/3",
                "adr": "ADR-0001",
            }
        ],
    )
    assert check_waiver_adr_links(root) == []
    write_waivers(
        root,
        [
            {
                "id": "W3",
                "rule": "r",
                "reason": "t",
                "owner": "@t",
                "expires": (
                    dt.datetime.now(dt.UTC).date() + dt.timedelta(days=5)
                ).isoformat(),
                "issue": "https://example.com/3",
                "adr": "ADR-0099",
            }
        ],
    )
    problems = check_waiver_adr_links(root)
    assert any("cites unknown ADR-0099" in p for p in problems)


def test_baseline_downgrades_known_findings(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / "m.py").write_text('"""Purpose."""\n')
    finding = "m.py:1: docstring"
    assert main(root) == 1
    (root / "waivers").mkdir(exist_ok=True)
    (root / "waivers" / "baseline.check-tree.json").write_text(json.dumps([finding]))
    assert main(root) == 0
    (root / "m.py").write_text('"""Other."""\n\n"stray"\n')
    assert main(root) == 1


def test_stale_baseline_entry_is_reported(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / "waivers").mkdir(exist_ok=True)
    (root / "waivers" / "baseline.check-tree.json").write_text(
        json.dumps(["gone.py:1: comment"])
    )
    proc = subprocess.run(
        [
            sys.executable,
            str(
                pathlib.Path(__file__).resolve().parents[1]
                / "scripts"
                / "check_tree.py"
            ),
            str(root),
        ],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "stale baseline entry" in proc.stdout


def test_json_output_lists_findings(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    (root / "m.py").write_text('"""Purpose."""\n')
    proc = subprocess.run(
        [
            sys.executable,
            str(
                pathlib.Path(__file__).resolve().parents[1]
                / "scripts"
                / "check_tree.py"
            ),
            str(root),
            "--format=json",
        ],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 1
    assert "m.py:1: docstring" in proc.stdout


def test_enforcement_must_name_a_real_artifact(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    write_adr(
        root,
        "0001",
        "one",
        adr_body("0001", "One").replace(
            "- Enforcement: review", "- Enforcement: `scripts/ghost.py`"
        ),
    )
    problems = check_adr_records(root)
    assert any("Enforcement names missing scripts/ghost.py" in p for p in problems)


def test_enforcement_must_name_a_real_function(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    write_adr(
        root,
        "0001",
        "one",
        adr_body("0001", "One").replace(
            "- Enforcement: review",
            "- Enforcement: `scripts/check_tree.py` (`check_ghost_rule`)",
        ),
    )
    scripts = root / "scripts"
    scripts.mkdir()
    (scripts / "check_tree.py").write_text("def check_real_rule():\n    return 1\n")
    problems = check_adr_records(root)
    assert any(
        "Enforcement names missing check_ghost_rule in scripts/check_tree.py" in p
        for p in problems
    )


def test_enforcement_review_is_exempt(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    write_adr(root, "0001", "one", adr_body("0001", "One"))
    assert not [p for p in check_adr_records(root) if "Enforcement" in p]


def test_adr_index_must_match_the_records(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    write_adr(root, "0001", "one", adr_body("0001", "One"))
    index = root / "docs" / "adr" / "README.md"
    index.write_text(
        "| ADR | Title | Status |\n|---|---|---|\n| 0001 | Wrong | accepted |\n"
    )
    problems = check_adr_records(root)
    assert any("title 'Wrong' != 'One'" in p for p in problems)


def test_adr_index_must_list_every_record(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    write_adr(root, "0001", "one", adr_body("0001", "One"))
    index = root / "docs" / "adr" / "README.md"
    index.write_text("| ADR | Title | Status |\n|---|---|---|\n")
    problems = check_adr_records(root)
    assert any("ADR-0001 is not listed" in p for p in problems)


def test_adr_index_status_must_match(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    write_adr(root, "0001", "one", adr_body("0001", "One"))
    write_adr(root, "0002", "two", adr_body("0002", "Two", status="superseded"))
    write_adr(root, "0003", "three", adr_body("0003", "Three", supersedes="ADR-0002"))
    index = root / "docs" / "adr" / "README.md"
    index.write_text(
        "| ADR | Title | Status |\n|---|---|---|\n"
        "| 0001 | One | accepted |\n"
        "| 0002 | Two | accepted |\n"
        "| 0003 | Three | accepted |\n"
    )
    problems = check_adr_records(root)
    assert any(
        "ADR-0002 status 'accepted' != 'superseded by 0003'" in p for p in problems
    )


def test_adr_index_rejects_unknown_rows(tmp_path: pathlib.Path) -> None:
    root = make_tree(tmp_path)
    write_adr(root, "0001", "one", adr_body("0001", "One"))
    index = root / "docs" / "adr" / "README.md"
    index.write_text(
        "| ADR | Title | Status |\n|---|---|---|\n"
        "| 0001 | One | accepted |\n"
        "| 0099 | Ghost | accepted |\n"
    )
    problems = check_adr_records(root)
    assert any("lists ADR-0099, which does not exist" in p for p in problems)
