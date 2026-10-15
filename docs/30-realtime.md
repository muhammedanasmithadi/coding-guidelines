# 30 Real-time APIs

- Protocol choice: SSE for server-push; WebSocket for bidirectional low-latency; HTTP/2 streaming for bulk; document the choice.
- Heartbeats and idle timeouts on every connection; close reason codes documented.
- Backpressure and bounded per-connection buffers; drop/degrade non-critical traffic under load; never unbounded fan-out.
- Reconnection is client-driven with exponential backoff + jitter; server is stateless with resumable cursors/tokens.
- Ordering guarantees documented per channel; messages carry idempotency keys; duplicates are safe.
- Auth on connect and per-message authorization where needed; tokens short-lived; rate limits per connection.
- Check: load test with k6/Artillery at 10x peak, soak test for leak detection, disconnect/reconnect chaos, latency/fanout budgets in `checks/performance-budgets.md`.
- Sources: RFC 6455 https://datatracker.ietf.org/doc/html/rfc6455, MDN Server-Sent Events https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events, WebSocket API https://developer.mozilla.org/en-US/docs/Web/API/WebSocket
- Waivers: `docs/waivers.md`.

## Examples

- `docs/17-concurrency.md` (queues, caps, circuit breaker)
- `docs/12-api-rest.md` (auth, pagination, idempotency)
- `checks/performance-budgets.md` (latency)