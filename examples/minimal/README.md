# Minimal adopter

Copy to new repo:

- `.editorconfig` (repo root, discovered upward)
- `.oxfmtrc.json`, `.oxlintrc.json` (repo root; oxfmt/oxlint configs — without them the tools run defaults and pass vacuously)
- `.pre-commit-config.yaml` (repo root; hooks reference `enforce/` configs)
- `checks/*.md` thresholds in CI
- `.github/workflows/quality.yml`
- `VERSION` + `CHANGELOG.md` (pin record; `check_tree` verifies they match)
- `docs/adr/0001-template.md` (decision record format; add your own `docs/adr/README.md` index once you have records)

Run: `pre-commit run --all-files`.
