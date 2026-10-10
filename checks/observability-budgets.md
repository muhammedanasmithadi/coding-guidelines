# Observability budgets (TEAM CHOICE, enforce as warning→blocking)

- Logs: ≤X GB/day/service. Drop DEBUG in prod. No PII/secrets. JSON to stdout only.
- Metrics: ≤N active series/service. Allowlist labels. Forbid `user_id`/`order_id` labels (cardinality kills Prometheus; check with `promtool`).
- Traces: head ≤1% above 10k RPS + tail 100% on errors/slow. Exemplars on histograms.
- Every paging alert links a runbook. No runbookless pages.
