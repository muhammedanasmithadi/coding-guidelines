# 08 Design

- SOLID: one reason to change (S), extend by addition (O), subtypes preserve contracts (L), small role interfaces (I), depend on abstractions (D).
- Outcome-oriented execution: optimize planned rewrites for the target design; temporary breakage is acceptable when planned, scoped, and reversible.
- Boundary discipline: validate once at the boundary, trust internal types; no duplicated validation along the call chain.
- Subtract before you add: remove dead code and redundant validators before building; prefer deletion over accumulation.
- Compose behaviors. Inject deps via constructor. Keep public surface small: package root re-exports only (`__all__`/barrel). No cycles (`api -> service -> repo`).
- Parse, don't validate: turn inputs into typed values at boundaries; unrepresentable states cannot be constructed anywhere else.
- Prefer total functions: no panics/exceptions for expected branches; handle every constructor of a union (exhaustive match).
- Check: `ruff --select I`, import-cycle check, export/API linters. Waivers: `docs/waivers.md`.

## Examples

- `examples/good-vs-bad/design-solid.md`, `structure.md`
