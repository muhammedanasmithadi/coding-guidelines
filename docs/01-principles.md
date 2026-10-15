# 01 Principles

- Write small pure functions. Return values. Avoid hidden state.
- Name reveals intent. No abbreviations except industry standard (`id`, `url`, `api`).
- Fail fast. Validate at boundary. Return typed errors.
- Delete duplication by abstraction only when the third use appears.
- Prefer composition over inheritance. Keep interfaces narrow.
- No comments in code. Code reads by reading it: names, structure, tests.
  Behavior is documented in README and docs, never beside the code. Banned:
  explanations of what code does, commented-out code, section banners, personal
  notes. Allowed: machine directives (`noqa`, `pragma`, `type:`, `fmt:`,
  `isort:`, shebang) and nothing else. Rationale that must survive lives in
  docs/ADRs with an ID, not in a comment.

Check: Ruff, ESLint, golangci-lint enforce size/complexity (see `docs/languages/`). `ERA001`/`F841` delete dead and commented-out code. Other languages per `docs/adr/0003-supported-languages.md`. Review enforces the rest — see PR checklist.
Sources: Clean Code, https://martinfowler.com/books/refactoring.html, https://web.stanford.edu/~ouster/cgi-bin/book.php, Parse, don't validate https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/, Make illegal states unrepresentable (common functional-programming practice).

## Examples

- `examples/good-vs-bad/design-solid.md` (S/O/L/I/D, composition, DI)
- `examples/good-vs-bad/functions.md` (size, CC<15)
- `examples/good-vs-bad/ai-slop.md` (AI failure modes + catches)
