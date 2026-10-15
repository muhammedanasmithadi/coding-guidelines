# 31 Classic engineering principles

- Hyrum's Law: any observable behavior becomes someone's dependency; design APIs, tests, and docs around the intended contract, not accidents.
- Orthogonality: unrelated concerns remain independent so changing one does not ripple through others (`docs/02-structure.md`, `docs/08-design.md`).
- Reversibility: keep decisions easy to change; prefer strategies/config over hard-coded policy; use ADRs for hard-to-reverse choices.
- Tracer bullets: ship a thin end-to-end slice first, then deepen; each commit is a working checkpoint (`docs/07-functions.md`, `docs/03-testing.md`).
- Broken windows: fix small defects and style violations on touch; ratchet baselines downward, never up.
- Clean Code (Robert C. Martin): names reveal intent, small functions, no hidden state, comments only for why-rationale in docs, tests are part of the product.
- Pragmatic Programmer: don't duplicate knowledge, keep knowledge in code, automate routine work, name things precisely.
- Design by Contract: preconditions at boundaries, postconditions at returns, invariants continuously checked in tests (`docs/09-errors.md`).
- SE at Google: readability review, design docs for cross-team changes, small CLs, deprecation and migration windows, blameless postmortems (`docs/05-commits.md`, `docs/09-errors.md`, `docs/incident.md`).
- Code smells: long method, large class, feature envy, shotgun surgery, primitive obsession, data clumps, switch statements on type tags, speculative generality; refactor before adding behavior.

Check: design reviews cite the rule being satisfied, `docs/codemods.md` for mass migrations, ADRs for irreversible choices, coverage/complexity gates for every change.
Sources: Robert C. Martin (Clean Code, Clean Architecture), The Pragmatic Programmer (Hunt & Thomas), Hyrum's Law (Wright), Software Engineering at Google (Winters, Manshreck, Wright).
Waivers: `docs/waivers.md`.

## Examples

- `docs/01-principles.md` (pure functions, naming, no comments in code)
- `docs/08-design.md` (composition, dependency inversion, parse don't validate)
- `docs/09-errors.md` (typed errors, exhaustive handling)
- `docs/05-commits.md` (small, intent-revealing commits)
- `docs/incident.md` (postmortem, blameless action items)
