# API / Versioning / Migrations — Do vs Avoid

Sources: Microsoft API https://github.com/microsoft/api-guidelines, SemVer https://semver.org/, proto3 https://protobuf.dev/programming-guides/proto3/#updating, GraphQL https://graphql.org/learn/pagination/

## REST naming

Do: `GET /customers/5/orders`, `POST /orders`
Avoid: `GET /create-order` — verb duplicates method. Deep `.../orders/99/products` couples URI to joins.

## Status codes

Do: `POST /orders -> 201 Location: /orders/123`, `DELETE -> 204`, bad input `400`, missing `404`, conflict `409`.
Avoid: `200 {success:false}` for all failures. Clients cannot retry/cache. Monitoring misses errors.

## Pagination

Do: `GET /orders?limit=25&offset=50 -> {value:[...], nextLink:...}`. Cap limit.
Avoid: unbounded `GET /orders` returning 2M rows. OOM, timeout. Adding paging later breaks.

## Idempotency

Do: `PUT /orders/client-uuid-1` retry-safe. `POST /charge` carries `Idempotency-Key` (Stripe term; Microsoft/Azure term is `Repeatability-Request-ID`).
Avoid: `POST /orders` creating duplicate on retry. Retry doubles charge.

## gRPC numbering

Do:
```proto
message Person { string name = 1; int32 id = 2; }
```

Avoid: renumber `id 2 -> 3` for style. Wire uses numbers. Old bytes decode to wrong field.

## gRPC compat

Do: add fields only, `reserve` deleted numbers. Avoid: `int32 -> string` change, reuse deleted number. Forces lockstep deploy.

## GraphQL pagination

Do: Relay `edges{cursor,node} + pageInfo{endCursor,hasNextPage}` with opaque cursor.
Avoid: `offset/limit`. Inserts skip/dupe rows. Large offsets scan table.

## GraphQL evolution

Do:
```graphql
name: String! @deprecated(reason: "Use firstName/lastName")
```

Avoid: `/graphql/v2` fork or silent removal. Fork doubles cost. Silent removal breaks clients.

## SemVer

Do: break -> MAJOR, add compat -> MINOR, fix -> PATCH. Never mutate released version.
Avoid: breaking change in `1.2.3 -> 1.2.4`. `^1.2.3` pulls breakage.

## DB expand-contract

Do:
```sql
-- 1 expand: ALTER TABLE users ADD COLUMN first_name TEXT;
-- 2 backfill batches; 3 switch readers; 4 drop old column
```

Avoid: single deploy renames `name -> first_name`. Old code writes missing column. Rollback fails.

## Docs-as-code / ADR

Do: `docs/api/orders.md` + `openapi.yaml` linted (`spectral lint`) with code. ADR `adr/0007-*.md` records context/decision.
Avoid: wiki edited out of band. Code ships, docs stale in 2 weeks.
