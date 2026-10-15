# 30 Real-time APIs

- Protocol choice: SSE for server-push; WebSocket for bidirectional low-latency; HTTP/2 streaming for bulk; document the choice.
- Heartbeats and idle timeouts on every connection: ping every 30s (TEAM CHOICE), idle timeout 60s; close reason codes documented.
- Backpressure and bounded per-connection buffers (drop oldest non-critical): never unbounded fan-out.
- Reconnection is client-driven with exponential backoff + jitter (1s initial, 30s cap) with max retries; server is stateless with resumable cursors/tokens.
- Ordering guarantees documented per channel; messages carry idempotency keys; duplicates are safe.
- Auth on connect and per-message authorization where needed; tokens short-lived (<=15m); rate limits per connection with numeric window; token TTL documented.
- Check: load test at 10x peak and soak for leak detection; chaos covers disconnect/reconnect and auth; targets p99 within budget, error rate <0.1%, memory growth <5%, fanout within budget (see `checks/performance-budgets.md`).
- Sources: RFC 6455 https://datatracker.ietf.org/doc/html/rfc6455, MDN Server-Sent Events https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events, WebSocket API https://developer.mozilla.org/en-US/docs/Web/API/WebSocket
- Waivers: `docs/waivers.md`.

## Examples

- `docs/17-concurrency.md` (queues, caps, circuit breaker)
- `docs/12-api-rest.md` (auth, pagination, idempotency)
- `checks/performance-budgets.md` (latency)

Sources: RFC 6455 https://datatracker.ietf.org/doc/html/rfc6455, MDN https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
