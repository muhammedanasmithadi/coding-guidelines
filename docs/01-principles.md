# 01 Principles

- Write small pure functions. Return values. Avoid hidden state.
- Name reveals intent. No abbreviations except industry standard (`id`, `url`, `api`).
- Fail fast. Validate at boundary. Return typed errors.
- Determinism first: pure functions for logic, explicit side effects, seeded randomness, no hidden global state in the domain layer.
- Functional core, imperative shell: domain logic pure and total; I/O and side effects at the edges.
- Defense in depth: validate at every trust boundary; never assume an internal caller is safe.
- Privacy by design: minimize PII, classify, retain/delete by policy; never log secrets.
- Crash-only software: design for restart; state recovery over graceful degradation when forced.
- Delete duplication by abstraction only when the third use appears.
- Prefer composition over inheritance. Keep interfaces narrow.
- Choose core data structures first; let downstream logic follow from them.
- Reader load is the real metric: minimize layers to trace and mutable state to hold; inline one-caller wrappers.
- Laziness protocol: prefer deletion, smallest change that solves the problem, no speculative layers.
- Outcome-oriented execution: converge planned rewrites on the target design; no throwaway compatibility states without a phase boundary.
- Attack the premise after two failed fixes: question the shared assumption, not another workaround.
- No comments in code. Avoid at all costs: add one only when absolutely required, and
  only because a named tool or external contract forces it. If you cannot name that
  tool or contract, the comment is banned. Rationale about an approach lives in an
  ADR (`docs/adr/`, format in `docs/adr/0008-rationale-routing.md`); rationale about a
  line lives in the code itself (names, types, structure, tests). Banned: explanations
  of what code does, commented-out code, section banners, TODO/FIXME/HACK, personal
  notes, module and function docstrings. Allowed: machine directives (`noqa`,
  `pragma`, `type:`, `fmt:`, `isort:`, `cspell:`, shebang, `#[allow]`, `#[expect]`,
  `@Suppress`, `//nolint`) and doc comments a mandated tool or contract requires (Go
  godoc on exported symbols per `docs/languages/go.md`; a published package's autodoc
  contract). Nothing else.

Check: Ruff, ESLint, golangci-lint enforce size/complexity (see `docs/languages/`). `ERA001`/`F841` delete dead and commented-out code. `scripts/check_tree.py` bans docstrings and block comments; `scripts/check-comments.sh` reports Rust/Kotlin/C/Go comments (advisory). Other languages per `docs/adr/0005-rust-and-c-support.md`. Review enforces the rest — see PR checklist.
Sources: Clean Code, https://martinfowler.com/books/refactoring.html, https://web.stanford.edu/~ouster/cgi-bin/book.php, Parse, don't validate https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/, Make illegal states unrepresentable (common functional-programming practice).

## Examples

- `examples/good-vs-bad/design-solid.md` (S/O/L/I/D, composition, DI)
- `examples/good-vs-bad/functions.md` (size, CC<15)
- `examples/good-vs-bad/comments-and-adrs.md` (comment ban, docstrings, ADR fields, supersede chain)
- `examples/good-vs-bad/ai-slop.md` (AI failure modes + catches)
