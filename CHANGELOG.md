# Changelog

Format follows https://keepachangelog.com/en/1.0.0/. Version follows https://semver.org/.

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
