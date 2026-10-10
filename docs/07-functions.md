# 07 Functions

- TEAM CHOICE gate (local policy, no PEP 8/Google source): <50 lines, <5 params, CC<15, file <200 LOC. Return early. No flag params, no 4-deep nesting.
- Pure where possible. Side effects at edges. One intent per function.
- Check: `lizard -C 15 -L 200 .`, `radon cc -s -n B`, Ruff `B`/`SIM`, ESLint complexity rules. Waivers: `docs/waivers.md`.

## Examples

- `examples/good-vs-bad/functions.md`, `python.md` §2, `typescript.md` §2
