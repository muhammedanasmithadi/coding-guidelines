# 16 Migrations, 17 Concurrency

## Migrations
- Expand-contract (aka Parallel Change). Reversible. Backfill in batches. No table rewrite without `CONCURRENTLY`.
- Lint: `squawk ./migrations/*.sql` (https://github.com/sbdchd/squawk).

## Concurrency
- Set timeout + deadline on every I/O. Cancel via context. Idempotency keys on POST/webhooks/queues (outbox pattern).
- Isolate with bulkhead. Break with circuit breaker: https://martinfowler.com/bliki/CircuitBreaker.html
