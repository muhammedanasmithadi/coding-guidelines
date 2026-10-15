# 07 Functions

- TEAM CHOICE gate (local policy, no PEP 8/Google source): <50 lines, <5 params, CC<15, file <200 LOC. Return early. No flag params, no 4-deep nesting. Calibrate <200 LOC to the service's measured module size (see `checks/performance-budgets.md`).
- Pure where possible. Side effects at edges. One intent per function.
- Blocking for new application code. Existing complex code (framework-scale hot spots) uses warning + waiver with justification — Django evidence: 1.7% breach, including battle-tested code (`Model.__new__` CC 68).
- Check: `lizard -C 15 -L 200 .`, Ruff `B`/`SIM`. Waivers: `docs/waivers.md`.

## Examples

- `examples/good-vs-bad/functions.md`, `python.md` §2, `typescript.md` §2
