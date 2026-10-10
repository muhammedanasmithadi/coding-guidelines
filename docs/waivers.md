# Waivers

Strict gates need an escape hatch with expiry. No silent `nolint`.

## Active waiver file

`waivers/active.yml` entries carry: rule, reason, owner, expires (max 90d), link to issue.

```yaml
- id: WAIV-001
  rule: complexity CC<15
  reason: legacy parser rewrite scheduled
  owner: @team-api
  expires: 2026-12-31
  issue: https://example.com/issues/123
```

## Rules

- `nolint`/`noqa`/`eslint-disable` must cite waiver ID: `# noqa: WAIV-001`.
- CI fails on expired waiver or missing approval.
- Baseline files for legacy live here too: `waivers/baseline.<tool>.json`.

## Examples

- `waivers/active.yml` (live waivers)
- `scripts/check_waivers.py` (CI enforcer)
