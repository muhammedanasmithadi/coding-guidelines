# 09 Errors

- Typed errors. No bare `except`, no swallow. Chain with `raise X from Y`. Map to contract: https://cloud.google.com/apis/design/errors
- Retry retryable only (timeouts, 503, connect errors — never 4xx charges). Backoff with full jitter. Every I/O carries timeout + deadline.
- Python: enable Ruff `BLE` (blind-except). TS: `Result<T,E>` for expected failures, `unknown` catch + `cause` for exceptional.
- Check: `ruff --select BLE`, `@typescript-eslint/no-explicit-any`. Waivers: `docs/waivers.md`.

## Examples
- `examples/good-vs-bad/errors.md`, `python.md` §4, `typescript.md` §4
