# Changelog

Format follows https://keepachangelog.com/en/1.0.0/. Version follows https://semver.org/.

## [0.13.0] - 2026-10-12
### Added
- oxlint 1.87.0 + oxfmt 0.72.0 replace eslint + prettier (50-100x / 30x faster; ESLint-compatible IDs, Prettier migrated config; 100/101 files agree, 1 TOML file improved). Service template keeps ESLint/Prettier configs (principles-first).
- `requirements-ci.txt` without black (ruff format canonicalizes identically, verified zero-diff).
- Hook rev bumps: editorconfig-checker 3.11.1, gitleaks v8.30.1 (CLI needs no license key).
### Evaluated, deferred with rationale
- `typescript@7.0.2` native tsc: real but breaking major — needs its own validation (plus typescript-eslint peer cap <6.1).
- Biome (568 rules < oxlint 871), typos (misses novel misspellings), convco (config incompat), `ty` (0.0.x pre-stable), uv audit (needs project layout), prek pilot (0.x bus factor), pre-commit-hooks v6 (major, review first).
- `@stoplight/spectral-cli` stays floating: pinning it imports 4 HIGH vulnerabilities into the audited tree.

## [0.12.2] - 2026-10-10

### Fixed

- CI fully green (6/6 quality jobs + CodeQL): pinned hook tool versions, docs job full history, first-party lychee scope, live SRE URL.

## [0.12.1] - 2026-10-10

### Fixed

- Dictionary word `lycheeignore`. Added `make release` (post-edit gates for version files) so version bumps cannot skip spell/tree again.

## [0.12.0] - 2026-10-10

### Fixed

- Scope discipline (every check declares exact file scope): cspell hook limited to md, lychee hook removed (CI action covers it), `.lycheeignore` excludes `node_modules`, PR checklist requires scope on new checks.

### Added

- Comment ban in code (`docs/01-principles.md`): behavior lives in README/docs, never beside code. Allowed: machine directives only (`noqa`, `pragma`, `type:`, shebang).
- `check_comments` gate in `check_tree.py` (Python exact via tokenize; JS/SH/YAML/TOML line-based with quote awareness). Caught 2 live violations on first run. Rationale moved to docs before stripping.

## [0.11.0] - 2026-10-10

### Fixed

- CI red causes: pre-commit config moved to root (action requires it), mypy yaml stubs (`types-pyyaml` + config-file in CI and Makefile), cspell full-glob parity, npm HIGHs resolved by upgrades.

### Added

- Latest verified toolchain: python 3.12.15, node 22.23.3, ruff 0.17, black 26, prettier 3.9.9, eslint 10, typescript 5.9.3, cspell 10, commitlint 21, gitleaks 8.30, semgrep 1.180, lizard 1.24. `requirements-ci.txt` pins CI deps; Dependabot monitors it.
- Django empirical evidence folded in: UP031 demoted, TID252 parent-only, CC warning+waiver framing, MI never-a-gate, B904/BLE001 recipes, harness-fidelity rule.
- AI-slop guardrails (`ai-slop.md`, PR checklist, S/C901/PLR/ERA/PT/TD rules) + agent task-evasion blocks.
- Mission-critical tier (`mission-critical.md`), freshness script, principles-first policy (tools are reference implementations).

### Removed

- `enforce/versions.lock` (duplicated lockfiles and rotted). Single source: `package.json` + lockfile, `requirements-ci.txt`, `.python-version`, `.nvmrc` — all read natively by tools and CI.

## [0.10.0] - 2026-10-10

### Added

- CI split into parallel jobs (lint, python, typescript, contract, docs, tree). Coverage gate runs in CI (was local-only).
- `examples/minimal/openapi.yaml`: pristine contract, spectral-clean. Contract job lints it every build.
- `codeql.yml`: CodeQL python+javascript analysis on push/PR/weekly.
- Deferred honestly: hadolint/squawk/k6/trivy/SBOM need repo targets that do not exist yet; recorded here, not faked.

## [0.9.0] - 2026-10-10

### Added

- Toolchain side verified for real: root `.prettierrc.json`, `eslint.config.mjs`, `tsconfig.json` (checkJs on configs). `prettier --write` normalized 62 files.
- Exact pins in `package.json` + `package-lock.json` committed. `versions.lock` extended (typescript, typescript-eslint, cspell, commitlint).
- Commitlint wired end-to-end (deps + CI step); history linted clean.

## [0.8.0] - 2026-10-10

### Fixed

- Validation pass: restored log-level definitions, restored 3 dropped source URLs, recorded ADR template wording change.
- Hardened `check_tree.py`: skips build artifacts (fixes red-on-clean-tree), filename-only orphan matching, `^## Examples` regex, crash-proof waiver/version handling, dangling-link check, package.json version enforcement.
- Closed wiring gaps: `package.json` 0.7.0, commitlint deps + CI step, `pyyaml`/`pytest` in CI deps, fixed 4 doc mistakes (config filename, docstring, typo, mypy scope), labeled fleet-vs-traffic rollout.
- Tests: 14 pass, 94% total. CSpell 0 on 67 files.

## [0.7.0] - 2026-10-10

### Added

- Split all consolidated stubs: 06/07/08/09, 10/11, 12/13/14/15, 16/17, 18/19/20/21/22/23 — each with rule+threshold+command+source+waiver+examples.
- Expanded `tooling.md`, `metrics.md` (export schema, anti-gaming). ADR-0003 defers Rust/Java/C# with entry rule.
- `scripts/check_tree.py` + 4 tests: enforces no-NUL/empty, VERSION==CHANGELOG, zero orphaned examples, every doc has Examples, waivers valid. Wired into `make check` and `quality.yml`.

## [0.6.0] - 2026-10-10

### Added

- Scale-out batch: keyset pagination fix, `scaling.md`, `structure.md`, `testing-gaps.md`, `commits.md`, `a11y-i18n.md` do-vs-avoid examples.
- Templates: threat-model, runbook, postmortem, `slo.yaml`, `flag.yaml`, ADR-0002, `languages/go.md`.
- Fleet docs: ownership, review-throughput, codemods, tech-debt, rollout, incident, multi-region, observability-budgets.
- Distribution: `scripts/check-drift.sh`, `bootstrap.sh`, `run-codemod.sh`, `.devcontainer`, `dependabot.yml`, breaking-change RFC template, `metrics/schema.json`, quality `concurrency`.
- Every doc now links its examples (0 orphaned files).

## [0.5.0] - 2026-10-10

### Fixed

- Verified every rule vs live sources. Relabeled invented numbers as TEAM CHOICE (50/5/15, 80%, L200, timeouts, SLO budgets, K8s sizes).
- Fixed SLO math (99.9%/30d≈43min, 28d≈40min), canary single standard 5%→25%→100%, `/livez`+`/readyz` (healthz deprecated), HPA-p95 adapter note.
- Fixed wiring: editorconfig action, local prettier-check/cspell hooks, lychee flag dropped, `squawk <files>` + correct URL, commitlint config + values, Go awk gate, JaCoCo note, cspell `--config`, `gitleaks dir`, ruff `BLE` + `ruff-check`, tsconfig + eslint missing flags, `[tool.lizard]` removed, waiver 90d + owner enforced.
- Added `commitlint.config.mjs`. CSpell 0 issues on 30 files.

## [0.4.0] - 2026-10-10

### Added

- Deep research pass: Python, TypeScript, SOLID/API, production resilience patterns with verified URLs.
- Full do-vs-avoid examples per pattern: `python.md`, `typescript.md`, `design-solid.md`, `api.md`, `production.md` + index `README.md`.
- Ruff-formatted embedded Python in markdown. Extended `cspell.yaml` dictionary. CSpell 0 issues on 8 files.

### Changed

- `examples/good-vs-bad/design-solid.md`, `python.md` reformatted to pass `ruff format`.

## [0.3.0] - 2026-10-10

### Added

- Self-verifying: `tests/test_check_waivers.py` (98% total, script 97%), `Makefile check/test`, `package.json`, git init.
- Refactored `scripts/check_waivers.py` to importable `find_expired()` + `main()` for testability. Renamed to `snake_case` per naming rule.

### Changed

- `Makefile test` reports `--include="scripts/*,tests/*"`.

## [0.2.0] - 2026-10-10

### Changed

- Strict gates: `tsc --noEmit` and `cspell` + `lychee` now block. Removed `|| true`.
- Fixed `pre-commit` hook IDs (`ruff-format`, `prettier`).

### Added

- `enforce/python/pyproject.toml` (ruff/black/coverage), `enforce/typescript/` (eslint/prettier/tsconfig), `enforce/cspell.yaml`, `enforce/.spectral.yaml`, `.gitignore`, `examples/full/`, `examples/good-vs-bad/errors.md`, audit issue template.
- Dogfooded: `scripts/check_waivers.py` passes ruff + black.

## [0.1.0] - 2026-10-10

### Added

- Initial scaffold: core docs, Python + TypeScript pilots, strict `quality.yml`, pre-commit, waivers, migration + audit docs.
