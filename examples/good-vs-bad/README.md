# Good vs Bad — index

Each file pairs Do with Avoid per pattern. Read the file for your change.

- `ai-slop.md` — AI failure modes + catches
- `c.md` — bounds, ownership, cleanup
- `rust.md` — ownership, Result, async
- `functions.md` — size, CC<15
- `errors.md` — typed errors, no swallow
- `python.md` — naming, purity, logging, config, pydantic, asyncio, pytest, Hypothesis, mypy
- `typescript.md` — narrowing, Result, zod, AbortController, testing, strict tsconfig
- `typescript-robust.md` — t3-env, tRPC, caller tests, exhaustive `never`
- `design-solid.md` — S/O/L/I/D, composition, DI, boundaries
- `api.md` — REST, gRPC, GraphQL, SemVer, expand-contract, docs, ADR
- `production.md` — logs, traces, RED/USE, breaker, probes, shutdown, secrets, auth, SQLi, Dockerfile, K8s, flags, SLOs
- `scaling.md` — keyset, cache, queues, concurrency caps, compat
- `testing-gaps.md` — quarantine, fake clock, mutation
- `commits.md` — conventional messages
- `a11y-i18n.md` — WCAG, ICU, UTC
- `structure.md` — public surface, layers, no cycles

Rule: copy the Do block. Cite the Avoid smell in PR if you see it.
