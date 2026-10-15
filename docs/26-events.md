# 26 Event-driven systems

- Schema is a contract: use a schema format (Avro/Protobuf/JSON Schema) with compatibility rules; breaking change = new major version with a 2-version migration window (`docs/23-deprecation.md`).
- Producers use outbox pattern and idempotency keys; consumers are idempotent and checkpoint only after side effects complete.
- Ordering: document ordering key and scope; never assume global order; handle duplicates and replays.
- DLQ + poison-pill handling with max 5 retries, exponential backoff capped at 5 min, and an alert; replay runbook in `docs/runbook-template.md`.
- Backpressure: bounded queues, lag alert when lag exceeds 5 minutes or 10,000 messages, consumer autoscaling on target utilization, drop/defer non-critical.
- Observability: trace propagation over `traceparent`, lag metrics, consumer error rate, poison-message counter.

Check: schema compatibility gate in CI (`buf breaking`/`jsonschema` diff), contract tests, chaos test (duplicate delivery, out-of-order, delay), DLQ alarm.
Sources: CloudEvents https://cloudevents.io/, Kafka docs https://kafka.apache.org/documentation/, Enterprise Integration Patterns https://www.enterpriseintegrationpatterns.com/
Waivers: `docs/waivers.md`.

## Examples

- `docs/17-concurrency.md` (queues, caps, exactly-once)
- `docs/15-versioning.md` (SemVer for schemas)
- `docs/runbook-template.md` (DLQ replay)
- `examples/good-vs-bad/scaling.md` (queues, caps, compat)
