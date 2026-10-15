# ADR 0006: Move runtimes to latest stable and LTS majors

- Status: accepted
- Context: The repo previously pinned Python 3.12 and Node 22 on every patch release while re-scanning majors quarterly.
- Decision: Track the active Python supported stable series and the active Node.js LTS major in .python-version and .nvmrc, and auto-bump their patch releases weekly through .github/workflows/runtime-bump.yml. Move to the next Python or Node major only when the current series enters end-of-life or an ADR requires it.
- Consequences: Adopters get a current runtime baseline without a manual six-month audit; patch bumps remain reviewable pull requests, and major runtime moves still require a new ADR.
