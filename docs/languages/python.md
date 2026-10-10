# Python

Sources: PEP 8 https://peps.python.org/pep-0008/, Google Python https://google.github.io/styleguide/pyguide.html

## Enforce

- Format: `black --check .` (line length 88, TEAM CHOICE override of PEP 8's 79 / Google's 80).
- Lint: `ruff check . --config enforce/python/pyproject.toml` (select E, F, I, B, BLE, UP, TID, SIM, TD, C901, PLR, S-subset, ERA, PT; `UP031` demoted — enforce f-string end state `UP032`; `TID252` parent-only).
- Types: `mypy scripts/` (strict via `enforce/python/pyproject.toml`; add `src/` when created).
- Test: `coverage run -m pytest && coverage report --fail-under=80` (80 = TEAM CHOICE).
- Complexity: `radon cc -s -n B src/`, `lizard -C 15 -L 200` (C15 = upstream default, L200 = TEAM CHOICE vs upstream 1000). MI is informational only, never a gate (floors at 0 on large cohesive files — Django evidence).

## Rules

- `snake_case` vars/functions, `CapWords` classes, `UPPER` consts.
- Imports sorted. No wildcard. Docstrings per PEP 257.
- Validate at boundary with pydantic https://docs.pydantic.dev/latest/.

## Examples

- `examples/good-vs-bad/python.md` (all 10 patterns)
- Waiver convention: `docs/waivers.md`
