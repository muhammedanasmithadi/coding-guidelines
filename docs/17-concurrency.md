# 17 Concurrency

- Timeout + deadline on every I/O. Cancel via context. Bound every fan-out with a pool/semaphore (TEAM CHOICE cap per downstream p99).
- Bounded queues, load shedding (`429/503 + Retry-After`), retry budgets (≤10% traffic, TEAM CHOICE), DLQ + poison-pill handling.
- Idempotency keys on POST/webhooks/queues with outbox + exactly-once-effect dedupe.
- Isolate with bulkhead. Break with circuit breaker: https://martinfowler.com/bliki/CircuitBreaker.html
- Check: lint bans unbounded fan-out and retry-on-4xx; k6 holds p99 at 10x. Waivers: `docs/waivers.md`.

## Examples
- `examples/good-vs-bad/production.md` (timeouts, breaker), `scaling.md` (queues, caps)
