# Scaling — Do vs Avoid

## Keyset pagination (not offset)

Do (opaque cursor over indexed keyset, `limit≤100` TEAM CHOICE):
```
GET /orders?after=opaque&limit=25
-- WHERE (created_at, id) > (?, ?) ORDER BY created_at, id LIMIT 25
```

Avoid: `GET /orders?offset=500000&limit=25`. Full scan + skip/dupe on inserts. p99 explodes at 100M rows.

## Cache-aside + singleflight

Do: `get(cache) → singleflight → DB → set(TTL 300s ± 10% jitter)`. Invalidate on write by event.

Avoid: every read hits DB. Cold restart herds DB into OOM. Fixed-TTL mass expiry stamps again.

## Bounded queues + shedding

Do: `Semaphore(100)` + queue cap 1000 + `429/503 + Retry-After` + DLQ. Retry budget ≤10% of traffic (TEAM CHOICE).

Avoid: unbounded inbox + infinite retry. Retry storm cascades at 10x traffic.

## Concurrency caps

Do:
```python
async with asyncio.Semaphore(50):
    await fetch(url)
```

Avoid: `await asyncio.gather(*[fetch(x) for x in range(1_000_000)])`. Spawns 1M tasks, OOMs host, DDoSes downstream.

## Compat readers

Do: additive-only JSON, tolerate unknown fields, enum defaults to `UNKNOWN`. Never tighten `required`.

Avoid: new `required` field or narrowed type. Breaks all old clients at fleet scale.
