# Good vs Bad — index

Each file pairs Do with Avoid per pattern. Read the file for your change.

- `functions.md` — size, CC<15
- `errors.md` — typed errors, no swallow
- `python.md` — naming, purity, logging, config, pydantic, asyncio, pytest, Hypothesis, mypy
- `typescript.md` — narrowing, Result, zod, AbortController, testing, strict tsconfig
- `design-solid.md` — S/O/L/I/D, composition, DI, boundaries
- `api.md` — REST, gRPC, GraphQL, SemVer, expand-contract, docs, ADR
- `production.md` — logs, traces, RED/USE, breaker, probes, shutdown, secrets, auth, SQLi, Dockerfile, K8s, flags, SLOs

Rule: copy the Do block. Cite the Avoid smell in PR if you see it.
