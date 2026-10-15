# 12 REST

- Fielding REST constraints, not fashion: stateless requests, cacheable responses, uniform interface, layered system. HATEOAS when the claim of REST matters — links describe allowed next actions; if you ship CRUD-only, call it HTTP+JSON and document the reduced model.
- Nouns, plurals, hierarchy max `collection/item/collection`. No verbs in paths. Sources: https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design, https://github.com/microsoft/api-guidelines, Fielding dissertation https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm
- Status exact: `200` read/update, `201+Location` create, `204` delete, `400` bad input, `404` missing, `409` conflict, `202+Location` async.
- Cacheability: `ETag`/`Last-Modified`, `Cache-Control` on GET, `304` on revalidation; mutable resources invalidate caches.
- Keyset pagination: opaque `after` cursor over `(created_at,id)` index, `limit≤100` (TEAM CHOICE). No `offset` at scale.
- Idempotency: `PUT` with client ID retry-safe. `POST` carries key (`Idempotency-Key`; Azure term `Repeatability-Request-ID`).
- Check: `spectral lint openapi.yaml`, `oasdiff breaking --fail-on ERR`, contract tests (Pact/provider verifier) against `openapi.yaml` in CI.
- Waivers: `docs/waivers.md`.

## Examples

- `examples/good-vs-bad/api.md` (naming, status, pagination, idempotency), `scaling.md` (keyset)
