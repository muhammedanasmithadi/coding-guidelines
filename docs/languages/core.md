# Core (language-agnostic musts)

Applies to all languages. Appendices add tool commands.

- Format on save. Final newline. Trim trailing space. UTF-8. LF.
- CC<15, file <200 LOC, function <50 lines. Coverage 80% lines/branches.
- No secrets in code. No TODO without issue link.
- Errors typed. Logs structured with trace ID.

Sources: PEP 8, Google style guides, Effective Go

## Examples

- `docs/languages/python.md`, `docs/languages/typescript.md`, `docs/languages/go.md`
- Waivers: `docs/waivers.md`
