# 04 Security

- Validate input at boundary (pydantic https://docs.pydantic.dev/latest/, zod https://zod.dev/).
- Auth: OAuth2 https://oauth.net/2/ + OIDC, short JWT, RBAC. No homegrown crypto.
- Threat model in PR for auth/billing/PII changes. Checklist: OWASP Top 10 https://owasp.org/www-project-top-ten/.
- Scan: `semgrep ci`, CodeQL https://codeql.github.com/, `gitleaks detect`, `pip-audit --strict`, `npm audit --audit-level=high`.
- Gate: 0 high/critical. Dependabot merges within 7d for critical.

No secrets in logs, URLs, or git history. Use Vault / cloud secret manager + rotation.
