# 10 Observability, 11 Config

## Logs
- Emit JSON. Include `trace_id`, `service`, `level`. No PII/secrets.
- Levels: DEBUG local, INFO prod path, WARN degraded, ERROR needs action.
- Source: https://12factor.net/logs, https://opentelemetry.io/docs/

## Metrics/Traces
- Track RED (rate/errors/duration) + USE. Propagate W3C Trace Context.
- Alert on burn rate, not raw errors.

## Config
- Read from env. Validate schema at boot. Fail fast on missing key.
- No hardcoded URLs/keys. Secrets come from manager (Vault / cloud) with rotation.
- Source: https://12factor.net/config

## Examples
- `examples/good-vs-bad/production.md` (logging, tracing, RED/USE)
- `examples/good-vs-bad/python.md` §5, `typescript.md` §6
