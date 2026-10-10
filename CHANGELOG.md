# Changelog

Format follows https://keepachangelog.com/en/1.0.0/. Version follows https://semver.org/.

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
