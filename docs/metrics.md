# Metrics

Track monthly, per service (schema: `metrics/schema.json`):

- Sonar new-code gate pass %, duplication %, maintainability rating.
- Patch coverage % (Codecov). Line/branch vs 80% floor (TEAM CHOICE).
- Waiver count + max age + baseline age. Alert on growth. No baseline older than 2 quarters without ADR.
- DORA: lead time p50, deploy frequency, change failure rate, MTTR p50.
- Anti-gaming: team-level only, never individual. Patch-coverage over line-only. Waiver rate uses denominator (waivers per KLOC). False-positive rate counterweights noisy rules.
- Export: monthly JSON per service to `metrics/`. Review in quarterly audit (`docs/audit.md`).

## Examples

- `metrics/schema.json`, `docs/tech-debt.md`, `docs/audit.md`
