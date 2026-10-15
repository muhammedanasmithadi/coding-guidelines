# 04 Security

- Validate input at boundary (pydantic https://docs.pydantic.dev/latest/, zod https://zod.dev/).
- Auth: OAuth2 https://oauth.net/2/ + OIDC, short JWT, RBAC. No homegrown crypto.
- Zero trust at boundaries: least-privilege service accounts, default-deny network policy, scoped credentials, provenance (SLSA level ≥2 for releases).
- Memory safety: no manual memory management; treat FFI/native deps as critical with sanitizers/fuzzing.
- Threat model in PR for auth/billing/PII changes. Checklist: OWASP Top 10 (2025) https://owasp.org/www-project-top-ten/ and OWASP ASVS https://owasp.org/www-project-application-security-verification-standard/ for verification depth.
- Scan: `semgrep ci`, CodeQL https://codeql.github.com/ (advisory unless required check), `gitleaks dir . -v`, `pip-audit --strict`, `npm audit --audit-level=high`, `osv-scanner scan --lockfile ...`, container image scan (trivy/grype).- Gate: 0 high/critical. Dependabot merges within 7d for critical.

No secrets in logs, URLs, or git history. Use Vault / cloud secret manager + rotation.

Sources: https://docs.pydantic.dev/latest/, https://zod.dev/, https://oauth.net/2/, https://owasp.org/www-project-top-ten/, https://owasp.org/www-project-application-security-verification-standard/, https://codeql.github.com/

## Examples

- `examples/good-vs-bad/ai-slop.md` (agent failure modes in this area)

- `examples/good-vs-bad/production.md` (secrets, auth, injection, Dockerfile, K8s)
- `docs/threat-model-template.md` (required for auth/billing/PII changes)
- `examples/good-vs-bad/ai-slop.md` (insecure defaults, hallucinated deps)
