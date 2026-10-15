# 27 Domain modeling

- Ubiquitous language lives in `CONTEXT.md` (glossary only; no implementation details). Rename code when the glossary renames a term.
- Bounded contexts are separate modules with explicit public surfaces; no cross-context deep imports (enforce with import-linter/dependency-cruiser).
- Make illegal states unrepresentable: discriminated unions, branded IDs, total functions, invariants enforced by constructors (not comments).
- Domain decisions with two real alternatives and high reversal cost become ADRs (`docs/21-adr.md`) using `docs/adr/` format.
- Stress-test relationships with concrete scenarios before coding; challenge fuzzy or overloaded terms.
- Parse, don't validate: untrusted data becomes typed domain values at the boundary; the rest of the code assumes validity.

Check: `CONTEXT.md` updated in the same PR as terminology changes; root README links to `CONTEXT.md` when present; ADR present for breaking domain decisions.
Sources: TypeScript advanced type patterns, Domain-Driven Design, parse-don't-validate essay.
Waivers: N/A (process doc, exempt from examples? Actually doc itself includes Examples).

## Examples

- `docs/21-adr.md` (decision records)
- `docs/02-structure.md` (boundaries, no cycles)
- `docs/08-design.md` (composition, parse don't validate)
- `examples/good-vs-bad/design-solid.md` (boundaries, DI)
