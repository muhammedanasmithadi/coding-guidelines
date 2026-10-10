# Threat model (required for auth/billing/PII changes)

- Scope: endpoints + data flows + trust boundaries (diagram or list).
- STRIDE per flow: spoofing, tampering, repudiation, info disclosure, DoS, elevation.
- OWASP Top 10 mapping: which A01-A10 apply, control for each.
- Abuse cases: rate limits, idempotency, authz per object (no IDOR).
- Residual risk + owner + review date.

## Examples

- `docs/04-security.md` (gates this template feeds)
- `examples/good-vs-bad/production.md` (auth, injection, secrets)
