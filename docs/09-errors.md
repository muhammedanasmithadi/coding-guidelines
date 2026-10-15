# 09 Errors

- Typed errors. No bare `except`, no swallow. Chain with `raise X from Y`. Map to contract: https://cloud.google.com/apis/design/errors
- Retry retryable only (timeouts, 503, connect errors — never 4xx charges). Backoff with full jitter. Every I/O carries timeout + deadline.
- Fix root causes: reproduce first, trace to cause, no nil-check guards that hide crashes; check all instances. Restart bug: suspect stale state before code.
- Python: enable Ruff `BLE` (blind-except). TS: `Result<T,E>` for expected failures, `unknown` catch + `cause` for exceptional.
- Invariants are executable: preconditions at boundaries, postconditions before return, structural assertions in tests. Never swallow `AssertionError`; treat as bug, not user error.
- Exhaustive handling: `match`/`switch` over closed sets must include a `never`/`assert never` branch; exhaustive `Result` match blocks forgotten cases.
- Check: `ruff --select BLE`, no-`any` rule (`typescript/no-explicit-any` under oxlint, `@typescript-eslint/no-explicit-any` in the service template). Waivers: `docs/waivers.md`.

Sources: https://cloud.google.com/apis/design/errors

## Examples

- `examples/good-vs-bad/errors.md`, `python.md` §4, `typescript.md` §4
