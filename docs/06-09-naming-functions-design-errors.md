# 06 Naming, 07 Functions, 08 Design, 09 Errors

## Naming
- Files: `snake_case.py`, `kebab-case.ts`, `SnakeCase.go` per language appendix.
- Vars/functions: verb or verb-phrase. Types: noun. Booleans: `is_`, `has_`, `can_`.
- Source: PEP 8 https://peps.python.org/pep-0008/

## Functions
- Keep <50 lines, <5 params, CC<15. Return early. No flag params.
- Pure where possible. Side effects at edges.

## Design
- SOLID. Compose. Inject deps. Keep public surface small.

## Errors
- Type errors. No bare `except`. No swallow. Map to contract: https://cloud.google.com/apis/design/errors
- Retry retryable only. Backoff+jitter. Set timeouts + deadlines.
