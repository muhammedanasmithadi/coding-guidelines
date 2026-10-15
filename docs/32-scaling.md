# 32 Scalability principles

- Stateless services behind load balancers; externalize session/state to backing stores; horizontal scale first, vertical only when measured.
- Capacity model per critical path: target RPS, concurrency, growth and headroom (2-3x) before production; load test in CI (k6/Artillery or equivalent) at 2-10x peak.
- Caching: cache-aside with TTL jitter; singleflight for cold paths; invalidate by event; stale-while-revalidate for user-facing reads.
- Data: keyset pagination; bounded queries; read replicas with lag-aware routing; partition only on proven hotspots; avoid distributed transactions.
- Backpressure: bounded queues, semaphores, retry budgets <=10%, load shedding (429/503 + Retry-After), DLQs with replay.
- Rate limits and tenant quotas at the edge; fair shedding, never unbounded fan-out.
- Observability of scale: saturation metrics (USE), latency percentiles, queue lag, cache hit rate; burn-rate alerts, not raw counts.
- Cost: budget per request/RPS; monitor cardinality and log volume (`checks/observability-budgets.md`).
- Check: load/soak/chaos results archived, capacity numbers in README, budgets in `checks/performance-budgets.md`.
  Sources: USE method https://www.brendangregg.com/usemethod.html, RED https://grafana.com/blog/2018/08/02/the-red-method-how-to-instrument-your-services/, SRE book https://sre.google/sre-book/table-of-contents/
- Waivers: `docs/waivers.md`.

## Examples

- `examples/good-vs-bad/scaling.md` (keyset, cache, queues, pools, compat)
- `docs/17-concurrency.md` (timeouts, caps, circuit breaker)
- `docs/15-versioning.md` (compat readers)
- `checks/performance-budgets.md` (budgets)
