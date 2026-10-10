# Onboarding (15 min)

1. Install pinned toolchain: `mise install` (see `enforce/versions.lock`).
2. Install hooks: `pre-commit install`.
3. Copy starter: `examples/minimal/` shows required files per repo.
4. Run local gates: `pre-commit run --all-files`.
5. Push. `quality.yml` runs the same commands and blocks merge on failure.
6. Ask: open discussion with repo link + failing log.

Start strict on new repos. Use `docs/migration.md` baseline + ratchet for legacy.

7. Browse `examples/good-vs-bad/README.md` for Do/Avoid per pattern.
8. For fleet use see `docs/ownership.md`, `docs/rollout.md`, `scripts/bootstrap.sh`, `.devcontainer/devcontainer.json`.
