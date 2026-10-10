# Changelog

Format follows https://keepachangelog.com/en/1.0.0/. Version follows https://semver.org/.

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
