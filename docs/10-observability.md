# 10 Observability

- Logs: JSON to stdout. Fields `trace_id`, `span_id`, `service`, `level`. No PII/secrets.
- Levels: DEBUG local only, INFO prod path, WARN degraded, ERROR needs action.
- Sources: https://12factor.net/logs, https://opentelemetry.io/docs/
- Traces: OTel SDK + OTLP + W3C `traceparent`. Head ≤1% above 10k RPS + tail 100% errors/slow (TEAM CHOICE).
- Metrics: RED per route + USE per node. Cardinality budget per `checks/observability-budgets.md`. Alert on burn, not raw errors.
- SLO/SLI + error budgets drive release policy; toil reduction tracked and eliminated.
- Check: OTel collector present, `promtool` cardinality, burn-rate alerts. Waivers: `docs/waivers.md`.

## Examples

- `examples/good-vs-bad/ai-slop.md` (agent failure modes in this area)

- `examples/good-vs-bad/production.md` (logging, tracing, metrics)
- `examples/good-vs-bad/python.md` §5, `typescript.md` §6

Sources: https://12factor.net/logs, https://opentelemetry.io/docs/
