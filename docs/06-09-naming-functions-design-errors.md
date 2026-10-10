# 06 Naming, 07 Functions, 08 Design, 09 Errors

## Naming
- PEP 8 mandates: `snake_case` modules/vars/functions, `CapWords` classes, `UPPER_SNAKE` consts. Never `l`/`O`/`I` alone. Source: PEP 8 https://peps.python.org/pep-0008/
- TEAM CHOICE (local, not PEP 8): files `snake_case.py`, booleans `is_/has_/can_`, verb-phrase functions, noun types.

## Functions
- TEAM CHOICE gate: <50 lines, <5 params, CC<15 (no PEP 8/Google source; local policy). Return early. No flag params.
- Pure where possible. Side effects at edges.

## Design
- SOLID. Compose. Inject deps. Keep public surface small.

## Errors
- Type errors. No bare `except`. No swallow. Map to contract: https://cloud.google.com/apis/design/errors
- Retry retryable only. Backoff+jitter. Set timeouts + deadlines.

## Examples
- `examples/good-vs-bad/python.md` §§1-4 (naming, functions, errors)
- `examples/good-vs-bad/typescript.md` §§1-4
- `examples/good-vs-bad/functions.md`, `errors.md`, `design-solid.md`
