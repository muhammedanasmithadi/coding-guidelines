# Multi-region

- Declare topology per tier: active-passive (Tier-0 write) vs active-active (Tier-2 read).
- Read-your-write: sticky region or read-after-write fence. No split-brain writes.
- RPO/RTO per tier + quarterly failover drill with measured times.
- Residency tags + replication allowlist. No PII where disallowed.

Sources: SRE workbook https://sre.google/workbook/table-of-contents/, region topology guidance

## Examples

- `examples/minimal/slo.yaml` (tier field), `docs/incident.md` (drill cadence)
