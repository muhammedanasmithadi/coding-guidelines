# Minimal adopter

Copy to new repo:

- `.editorconfig` (repo root, discovered upward)
- `.pre-commit-config.yaml` (repo root; hooks reference `enforce/` configs)
- `checks/*.md` thresholds in CI
- `.github/workflows/quality.yml`

Run: `pre-commit run --all-files`.
