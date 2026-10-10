# 08 Design

- SOLID: one reason to change (S), extend by addition (O), subtypes preserve contracts (L), small role interfaces (I), depend on abstractions (D).
- Compose behaviors. Inject deps via constructor. Keep public surface small: package root re-exports only (`__all__`/barrel). No cycles (`api -> service -> repo`).
- Check: `ruff --select I`, `eslint import/no-cycle`, export/API linters. Waivers: `docs/waivers.md`.

## Examples
- `examples/good-vs-bad/design-solid.md`, `structure.md`
