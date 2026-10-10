# 11 Config

- Read from env. Validate schema at boot. Fail fast on missing key. Source: https://12factor.net/config
- No hardcoded URLs/keys. Secrets from manager (Vault / cloud / ExternalSecrets) with rotation. Never log secrets.
- Config changes roll like code: canary per region, boot-validation distinguishes fatal vs degrade.
- Check: schema-validated config (`cuelang`/JSON-schema in CI), `gitleaks dir . -v`. Waivers: `docs/waivers.md`.

## Examples

- `examples/good-vs-bad/python.md` §6 (pydantic-settings), `production.md` (secrets)
