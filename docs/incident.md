# Incident management

- SEV1 (critical user impact) → SEV4 (cosmetic). Response times per SEV in runbook.
- On-call rotation + escalation required per service. No unowned alerts.
- Every paging alert links a runbook (`docs/runbook-template.md`).
- Postmortem within 48h (`examples/minimal/postmortem.md`). Action items carry owner + date.
- Quarterly game day (kill pod, inject latency, AZ failover). Record in `docs/audit.md`.

Sources: SRE book https://sre.google/sre-book/table-of-contents/

## Examples

- `docs/runbook-template.md`, `examples/minimal/postmortem.md`, `examples/minimal/slo.yaml`
