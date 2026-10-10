# Tooling

- Pin every check in `enforce/versions.lock` (ruff, black, prettier, eslint, node, python, gitleaks, semgrep, lizard). Weekly Dependabot bump (`.github/dependabot.yml`).
- Lockfiles required: `package-lock.json`, `poetry.lock`/`uv.lock`, `Cargo.lock`, `go.sum`. CI fails without them.
- Bump validation: owner approves, `examples/` CI runs green against new versions before rollout (`docs/rollout.md`).
- Consumers pin this repo by tag (`VERSION` + `CHANGELOG.md`). Drift check: `scripts/check-drift.sh <tag>` (advisory).

## Examples

- `enforce/versions.lock`, `scripts/check-drift.sh`, `scripts/bootstrap.sh`
