# Security gates

- `semgrep ci` — 0 blocking findings.
- CodeQL — 0 high/critical on new code.
- `gitleaks detect --source . --no-git` — 0 leaks.
- `pip-audit --strict` / `npm audit --audit-level=high` — 0 high/critical.
- Dependabot critical merges within 7d.

SBOM per release: `cyclonedx-py -o sbom.json`.
