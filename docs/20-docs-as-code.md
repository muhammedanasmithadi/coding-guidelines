# 20 Docs as code

- Docs live in-repo as Markdown, reviewed in PRs, versioned with code. Source: https://www.writethedocs.org/guide/docs-as-code/
- API docs generate from `openapi.yaml`/proto. Doc comments linted. No wiki edited out of band.
- Check: `lychee "**/*.md"`, `cspell --config enforce/cspell.yaml`. Waivers: `docs/waivers.md`.

## Examples
- `examples/minimal/README.md` (skeleton this doc's rule produces)
