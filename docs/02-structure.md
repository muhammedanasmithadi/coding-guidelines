# 02 Structure

- One module owns one concept. Public API lives in `__init__`/`index`/`lib.rs` only.
- Depend inward. No cycles. Workspace boundaries explicit (`monorepo.tools`: https://monorepo.tools/).
- Layout per repo:
  ```
  src/           # product code
  tests/         # mirrors src/
  docs/adr/      # decisions
  migrations/    # reversible DB changes
  openapi.yaml   # contract if service exposes HTTP
  ```
- No cross-package deep imports. Import the package root.

Check: import linters (`ruff --select I`, `eslint import/no-cycle`, `go list -deps` cycle check).
