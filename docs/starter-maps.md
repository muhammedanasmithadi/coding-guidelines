# Starter maps: what to copy per stack

Copy only your stack's files, then run its verify commands. Full adoption still
ends at `docs/adoption.md`.

## Python service

Copy:

- `enforce/python/pyproject.toml` (ruff, coverage, mypy config)
- `requirements-ci.txt` (pinned CI toolchain)
- `.python-version` (runtime pin, read by mise + setup-python)
- `.editorconfig`, `.pre-commit-config.yaml` (shared hygiene)
- `checks/coverage-thresholds.md`, `checks/performance-budgets.md` (thresholds)
- The `python` job from `.github/workflows/quality.yml`

Verify:

- `ruff check . --config enforce/python/pyproject.toml`
- `ruff format --check . --config enforce/python/pyproject.toml`
- `mypy . --config-file enforce/python/pyproject.toml`
- `coverage run -m pytest && coverage report --fail-under=80`

## TypeScript service

Copy:

- `enforce/typescript/tsconfig.json` (strict + `noUncheckedIndexedAccess`)
- `enforce/typescript/eslint.config.mjs` (strictTypeChecked template)
- `.oxfmtrc.json`, `.oxlintrc.json` (repo format + lint; migrate from Prettier/ESLint per `docs/languages/typescript.md`)
- `.nvmrc` (runtime pin, read by mise + setup-node)
- `.editorconfig`, `.pre-commit-config.yaml` (shared hygiene)
- The `typescript` + `contract` jobs from `.github/workflows/quality.yml`

Verify:

- `oxfmt --check .`
- `oxlint --max-warnings 0 .`
- `tsc --noEmit`
- `spectral lint openapi.yaml -r enforce/.spectral.yaml` (if an HTTP contract exists)

## Go service

Copy:

- `docs/languages/go.md` (rules; no enforce configs exist yet — `gofmt` + `go vet` ship with the toolchain)
- `.editorconfig`, `.pre-commit-config.yaml` (shared hygiene)
- `checks/coverage-thresholds.md` (80% gate + `awk` enforcement line)

Verify:

- `gofmt -l .` (empty output)
- `go vet ./...`
- `go test -coverprofile=cover.out ./... && go tool cover -func=cover.out | awk '/total:/{exit ($3+0<80)}'`

## Minimal read set (for agents)

- Start: `docs/01-principles.md`, `docs/languages/core.md`, your language appendix.
- Change feature: add `03-testing.md`, `07-functions.md`, `08-design.md`, `09-errors.md`.
- Change API: add `12/13/14-api-*.md`, `15-versioning.md`, `23-deprecation.md`.
- Change prod path: add `10-observability.md`, `17-concurrency.md`, `production.md`, `checks/performance-budgets.md`.
- Change data/event: add `25-data.md`, `26-events.md`, `16-migrations.md`.
- Then follow `check_*.py` and `make check`.

## Examples

- `docs/adoption.md` (done checklist), `docs/languages/` (per-language rules)
