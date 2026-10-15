# 06 Naming

- PEP 8 mandates: `snake_case` modules/vars/functions, `CapWords` classes, `UPPER_SNAKE` consts. Never `l`/`O`/`I` alone. Source: https://peps.python.org/pep-0008/
- TS: `camelCase` vars/functions, `PascalCase` types, `CONSTANT_CASE` globals. Source: https://google.github.io/styleguide/tsguide.html#naming
- TEAM CHOICE (local, not PEP 8): files `snake_case.py`, booleans `is_/has_/can_`, verb-phrase functions, noun types.
- Check: Ruff (`E`, `I`), ESLint naming rules. Waivers: `docs/waivers.md` (cite ID in `noqa`/disable).

Sources: https://peps.python.org/pep-0008/, https://google.github.io/styleguide/tsguide.html#naming

## Examples

- `examples/good-vs-bad/ai-slop.md` (agent failure modes + catches)

- `examples/good-vs-bad/python.md` §1, `typescript.md` §1
