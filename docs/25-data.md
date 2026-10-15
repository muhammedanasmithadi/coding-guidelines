# 25 Data correctness

- Transaction boundary equals use-case boundary. One transaction per request; no long-lived transactions (abort >5s). Retry on deadlock/serialization failure at most 3 times with full jitter and an idempotency key.
- Isolation: default READ COMMITTED; stronger levels only with measured need. Explain every new index and lock.
- Backfill with bounded batches (`LIMIT 1000`, off-peak, throttled, kill-switch); never table rewrite without `CONCURRENTLY` (expand-contract).
- Referential integrity enforced in DB, not only app. Migrations reversible and tested on production-like volume (dry-run + rollback drill).
- PII: classify, minimize, retain/delete per policy, encrypt at rest, audit access; test restore (RPO/RTO).
- Query discipline: <5 queries per request, no N+1, explain (analyze) new queries; budgets in `checks/performance-budgets.md`.
- Backup verification monthly: automated restore drill into isolated env, compare row counts and checksums.

Check: `squawk` migrations, `EXPLAIN (ANALYZE, BUFFERS)`, integration test against real DB engine (no mock DB), restore drill log.
Sources: PostgreSQL docs https://www.postgresql.org/docs/current/, 12factor backing services https://12factor.net/backing-services, SRE book https://sre.google/workbook/table-of-contents/
Waivers: `docs/waivers.md`.

## Examples

- `docs/16-migrations.md` (expand-contract)
- `docs/17-concurrency.md` (timeouts, breaker, outbox)
- `examples/good-vs-bad/production.md` (SQLi, transactions)
- `checks/performance-budgets.md` (DB budgets)
