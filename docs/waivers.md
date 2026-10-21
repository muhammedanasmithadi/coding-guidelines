# Waivers

Strict gates need an escape hatch with expiry. No silent `nolint`.

## Active waiver file

`waivers/active.yml` entries carry: rule, reason, owner, expires (max 90d), link to issue, and the ADR the exception bends (optional `adr` field).

```yaml
- id: WAIV-001
  rule: complexity CC<15
  reason: legacy parser rewrite scheduled
  owner: @team-api
  expires: 2026-12-31
  issue: https://example.com/issues/123
  adr: ADR-0008
```

## Rules

- `nolint`/`noqa`/`eslint-disable` must cite waiver ID: `# noqa: WAIV-001`.
- CI fails on expired waiver or missing approval.
- An `adr` field must name a record that exists in `docs/adr/`.
- Baseline files for legacy live here too: `waivers/baseline.<tool>.json`.

## Ratchet

`waivers/baseline.check-tree.json` holds the `scripts/check_tree.py` findings an
adopting repo accepts today. A finding in the baseline is reported as `baseline:` and
does not fail CI; a new finding does. `scripts/make-baseline.sh` writes both baselines.
A baseline entry with no matching finding is reported as `stale baseline entry` — remove
it. Baselines are committed and reviewed like any other file, so the burn-down is
visible in history.

Sources: docs/waivers.md

## Examples

- `waivers/active.yml` (live waivers)
- `scripts/check_waivers.py` (CI enforcer)
