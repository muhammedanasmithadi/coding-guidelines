# Ownership

Global `CODEOWNERS` routes to 3 teams. At scale add per-service fragments:

```
/services/<name>/ @team-<name>
/libs/<name>/ @team-<name>
enforce/ @platform-team
```

- Fallback owner required on every path. No ownerless directory.
- Review SLA: first review 24h, nudge 48h (stale-review bot).
- Appeals keep 5d SLA (`docs/appeals.md`). Gate contests do not block security fixes.

## Examples

- `docs/ownership.md` (this file), `CODEOWNERS`, `docs/appeals.md`
