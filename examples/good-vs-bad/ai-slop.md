# AI-generated slop — Do vs Avoid

AI assistants produce fluent, confident, often-wrong code. These 14 patterns are
the observed failure modes, each with its machine catch or review gate.
Evidence: Spracklen et al. https://arxiv.org/abs/2406.10279, Perry et al. https://arxiv.org/abs/2211.03622, StackOverflow 2024 https://survey.stackoverflow.co/2024/ai, DORA 2024 https://dora.dev/research/2024/dora-report/

## Machine-caught (ruff select in `enforce/python/pyproject.toml`)

- Swallowed exceptions with reassuring comments → `BLE001`, `S110`, `S112`, bare `except` → `E722`.
- Lost tracebacks (`raise X` inside `except`) → `B904`. Always `raise ... from err`.
- Insecure defaults (`verify=False`, `shell=True`, `random` tokens, raw SQL) → `S501`, `S602`, `S311`, `S608` (+ `S113` missing timeout, `S502` weak SSL).
- God-functions → `C901`, `PLR0912`, `PLR0915`. Magic literals → `PLR2004`.
- Dead/commented code → `ERA001`, `F841`. Stale imports → `UP035` (with `target-version` set).
- Vacuous asserts (`assert True`, `x == x`) → `S101` (production code), `B011`, `PT018` + mutation testing for true vacuity.

## Review-only (no verified rule exists — checklist enforced)

1. Over-mocked tests (`assert mock.called`): require ≥1 assertion on real observable state.
2. Hallucinated APIs/packages (5.2% commercial / 21.7% open-source imports hallucinated — Spracklen): verify against installed version (`mypy --strict`, import smoke test, lockfile + audit).
3. Copy-paste duplication: 3rd copy forces extraction (Sonar/`jscpd` duplication gate where available).
4. Defensive `None`-hedges hiding contracts: `mypy --strict`, `Optional` only at true boundaries.
5. New-dependency-per-task: lockfile-diff CI check — every new dep needs justification; stdlib first.
6. Comment-code mismatch + test-free "verified ✅": every behavior claim cites a test name or log. No proof, no merge.

## Agent task-evasion (forced completion)

AI agents dodge work with plausible comments. These are blocking review findings:

- Placeholder TODOs instead of the fix (`# TODO: handle edge case` with no issue link) → `TD` rules + waiver-ID requirement. A TODO without owner/issue is unfinished work, not a note.
- Gutted tests (`pytest.skip`, commented asserts) to turn red green → CI fails on skips without linked issue; coverage must not drop.
- Broad `except` + "handled elsewhere" with no handler named → `BLE001`; name the handler or let it propagate.
- "Out of scope" with no follow-up issue → file the issue in the same PR or do the work.
- Fake completion summaries ("all tests pass", "verified") → each claim links its artifact (test node ID, CI run URL, command output). Unlinked claims are treated as untested.
