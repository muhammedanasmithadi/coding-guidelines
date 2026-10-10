# TypeScript

Sources: Google TS https://google.github.io/styleguide/tsguide.html, Airbnb https://github.com/airbnb/javascript

## Enforce

- Format: `prettier --check .`
- Lint: `eslint . --max-warnings=0`
- Types: `tsc --noEmit` strict true.
- Test: `jest --coverage` with 80% lines/branches gate.
- Contract: `spectral lint openapi.yaml` if service exposes HTTP.

## Rules

- `camelCase` vars/functions, `PascalCase` types, `UPPER_SNAKE` consts.
- No `any` without waiver. Prefer `unknown` + narrow.
- Validate at boundary with zod https://zod.dev/.

## Examples
- `examples/good-vs-bad/typescript.md` (all 8 patterns)
- Waiver convention: `docs/waivers.md`
