# 20 Docs as code

- Docs live in-repo as Markdown, reviewed in PRs, versioned with code. Source: https://www.writethedocs.org/guide/docs-as-code/
- Encode lessons in structure: once advice is written twice, turn it into a lint rule, metadata flag, runtime check, or script; delete the prose.
- API docs generate from `openapi.yaml`/proto. Doc comments linted. No wiki edited out of band.
- Format: root `.oxfmtrc.json` (migrated from Prettier config via `oxfmt --migrate=prettier`; same printWidth/singleQuote/trailingComma, `proseWrap: preserve` keeps prose diffs small, code fences still formatted).
- Check: `lychee "**/*.md"`, `cspell --config enforce/cspell.yaml`, `oxfmt --check .`. Waivers: `docs/waivers.md`.

Sources: https://www.writethedocs.org/guide/docs-as-code/

## Examples

- `examples/minimal/README.md` (skeleton this doc's rule produces)
