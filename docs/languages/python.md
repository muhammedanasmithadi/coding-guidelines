# Python

Sources: PEP 8 https://peps.python.org/pep-0008/, Google Python https://google.github.io/styleguide/pyguide.html

## Enforce

- Format: `black --check .` (line length 88).
- Lint: `ruff check .` (select I, TID, B, UP).
- Types: `mypy src/` where typed.
- Test: `coverage run -m pytest && coverage report --fail-under=80`.
- Complexity: `radon cc -s -n B src/`, `lizard -C 15 -L 200`.

## Rules

- `snake_case` vars/functions, `CapWords` classes, `UPPER` consts.
- Imports sorted. No wildcard. Docstrings per PEP 257.
- Validate at boundary with pydantic https://docs.pydantic.dev/latest/.
