# coding-guidelines

Docs + enforcing configs + verified CI. Each rule maps to a command. CI blocks merge on failure.

## Use

1. Read `docs/onboarding.md`.
2. Copy `enforce/` + `checks/` + `.github/workflows/quality.yml` into your repo.
3. Run `pre-commit run --all-files`. Fix failures. Push. CI runs the same commands.
4. Pin version: reference this repo by tag `vX.Y.Z` (see `VERSION`, `CHANGELOG.md`).

## Layout

- `docs/` — rules. `docs/languages/` — per-language appendices.
- `enforce/` — `.editorconfig`, `pre-commit`, formatter/linter configs, pinned versions.
- `checks/` — thresholds that fail CI.
- `examples/` — minimal/full adopters + good-vs-bad diffs. CI tests them against current configs.
- `waivers/` — temporary exceptions with expiry. CI fails on expired waiver.

## Versioning

MAJOR = breaking gate. MINOR = new check. PATCH = fix/clarify. See `CHANGELOG.md`.

## Licenses

Code/configs/examples: Apache-2.0. Docs: CC-BY-4.0. See `LICENSE`.
