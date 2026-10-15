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

Check: import linters (`ruff --select I`, import-cycle check, `go list -deps` cycle check).

Sources: https://monorepo.tools/

## Examples

- `examples/good-vs-bad/ai-slop.md` (agent failure modes + catches)

- `examples/good-vs-bad/design-solid.md` (boundaries, no cycles)
- `examples/good-vs-bad/structure.md` (root vs deep imports)
