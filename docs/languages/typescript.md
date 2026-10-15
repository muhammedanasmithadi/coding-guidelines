# TypeScript

Sources: Google TS https://google.github.io/styleguide/tsguide.html, Airbnb https://github.com/airbnb/javascript

## Enforce

- Format: `oxfmt --check .` (oxfmt 0.x beta, Prettier-compatible; config migrated via `oxfmt --migrate=prettier`; 100/101 files agree with Prettier, 1 TOML file strictly improved).
- Lint: `oxlint --max-warnings 0 .` (oxlint 1.x, ESLint-compatible IDs: `eslint/no-unused-vars`, `eslint/no-empty`, `eslint/no-warning-comments`, `typescript/no-explicit-any`, plus `no-floating-promises` and `no-misused-promises` where type info is available; disable comments honored). 50–100x faster than ESLint; drops ~250 toolchain packages.
- The `enforce/typescript/` configs stay as an alternate service template (principles-first: teams choose either stack). Root uses oxlint/oxfmt.
- Types: `tsc --noEmit` strict true.
- Test: `jest --coverage` with 80% lines/branches gate.
- Contract: `spectral lint openapi.yaml` if service exposes HTTP.

## Rules

- `camelCase` vars/functions, `PascalCase` types, `UPPER_SNAKE` consts.
- No `any` without waiver. Prefer `unknown` + narrow.
- Validate at boundary with zod https://zod.dev/.

## Examples

- `examples/good-vs-bad/typescript.md` (all 8 patterns)
- `examples/good-vs-bad/typescript-robust.md` (t3-env, tRPC, caller tests, exhaustive `never`)
- Template validity is proven by import smoke test in `quality.yml`.
- Waiver convention: `docs/waivers.md`
