# 16 Migrations, 17 Concurrency

## Migrations
- Expand-contract. Reversible. Backfill in batches. No table rewrite without `CONCURRENTLY`.
- Lint: `squawk lift ./migrations/*.sql` (https://github.com/squawklabs/squawk).

## Concurrency
- Set timeout + deadline on every I/O. Cancel via context. Idempotency keys on POST/webhooks/queues (outbox pattern).
- Isolate with bulkhead. Break with circuit breaker: https://martinfowler.com/bliki/CircuitBreaker.html
