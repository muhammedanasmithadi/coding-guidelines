# Codemods (mass migration)

Breaking gate (MAJOR) ships with a codemod, not manual edits:

- `codemods/<rule>/sgconfig.yml` (ast-grep) + `scripts/run-codemod.sh`.
- Open auto-PR to all adopters. Ratchet after merge (`docs/migration.md`).
- Rule PRs require codemod artifact or written why-not (`CONTRIBUTING.md` checklist).

## Examples

- `scripts/run-codemod.sh`, `scripts/make-baseline.sh`
