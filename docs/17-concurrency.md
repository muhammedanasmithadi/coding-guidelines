# 17 Concurrency

- Timeout + deadline on every I/O. Cancel via context. Bound every fan-out with a pool/semaphore (TEAM CHOICE cap per downstream p99).
- Separate before serializing shared state: remove shared mutable state before adding locks/queues; make operations idempotent so retries converge.
- Concurrency corollary: isolate state; ask what happens if another actor mutates it before sharing.
- Bounded queues, load shedding (`429/503 + Retry-After`), retry budgets (≤10% traffic, TEAM CHOICE), DLQ + poison-pill handling.
- Idempotency keys on POST/webhooks/queues with outbox + exactly-once-effect dedupe.
- Isolate with bulkhead. Break with circuit breaker: https://martinfowler.com/bliki/CircuitBreaker.html
- Tail latency: hedge or replicate only hot requests; backpressure and load shedding before retry storms.
- Run sanitizers in CI: `go test -race`, TS `no-floating-promises`, Python `asyncio` task cancellation tests; stress with `-count=100` on changed paths.
- Deterministic concurrency tests use seeded schedulers/chaos injection; never depend on wall clock or thread scheduling.
- Check: lint bans unbounded fan-out and retry-on-4xx; k6 holds p99 at 10x. Waivers: `docs/waivers.md`.

Sources: https://martinfowler.com/bliki/CircuitBreaker.html

## Examples

- `examples/good-vs-bad/production.md` (timeouts, breaker), `scaling.md` (queues, caps)
