# 01 Principles

- Write small pure functions. Return values. Avoid hidden state.
- Name reveals intent. No abbreviations except industry standard (`id`, `url`, `api`).
- Fail fast. Validate at boundary. Return typed errors.
- Delete duplication by abstraction only when the third use appears.
- Prefer composition over inheritance. Keep interfaces narrow.

Check: Ruff, ESLint, golangci-lint enforce size/complexity (see `docs/languages/`). Other languages per `docs/adr/0003-supported-languages.md`. Review enforces the rest — see PR checklist.
Sources: Clean Code, https://martinfowler.com/books/refactoring.html, https://web.stanford.edu/~ouster/cgi-bin/book.php

## Examples
- `examples/good-vs-bad/design-solid.md` (S/O/L/I/D, composition, DI)
- `examples/good-vs-bad/functions.md` (size, CC<15)
