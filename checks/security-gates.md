# Security gates

- Semgrep `p/default` at ERROR severity on `scripts/` in CI (`semgrep` job) — 0 findings today. (`semgrep ci` proper needs an App token; the scan form covers the rule without one.)
- CodeQL — 0 high/critical on new code (configure as a required branch check to enforce).
- `gitleaks dir . -v` — 0 leaks.
- `pip-audit --strict` / `npm audit --audit-level=high` — 0 high/critical (TEAM CHOICE).
- Dependabot critical merges within 7d (TEAM CHOICE SLA).

SBOM per release: `cyclonedx-py requirements -o sbom.json` (v7+ requires subcommand).
