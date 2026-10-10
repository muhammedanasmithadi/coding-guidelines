# Security gates

- `semgrep ci` — 0 blocking findings (TEAM CHOICE: strict-zero needs waiver process).
- CodeQL — 0 high/critical on new code.
- `gitleaks dir . -v` — 0 leaks.
- `pip-audit --strict` / `npm audit --audit-level=high` — 0 high/critical (TEAM CHOICE).
- Dependabot critical merges within 7d (TEAM CHOICE SLA).

SBOM per release: `cyclonedx-py requirements -o sbom.json` (v7+ requires subcommand).
