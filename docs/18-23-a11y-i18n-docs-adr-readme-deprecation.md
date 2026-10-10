# 18 A11y, 19 I18n, 20 Docs-as-code, 21 ADR, 22 README, 23 Deprecation

- A11y: meet WCAG 2.2 AA https://www.w3.org/TR/WCAG22/. Check: `axe` in CI for web.
- I18n: ICU messages, UTC storage, CLDR formatting. No hardcoded strings/dates.
- Docs-as-code: lint doc comments + markdown links. `lychee **/*.md`, `cspell`. Source: https://www.writethedocs.org/guide/docs-as-code/
- ADR: record in `docs/adr/NNNN-title.md` for MAJOR gate changes. Template: context, options, decision, rollout.
- README: required sections — purpose, setup, run, test, deploy, owners, license. Template in `examples/minimal/README.md`.
- Deprecation: announce 2 versions ahead. Emit `Sunset`/`Deprecation` header. Remove after window.

## Examples
- `examples/good-vs-bad/a11y-i18n.md` (a11y, i18n)
- `examples/good-vs-bad/commits.md` (changelog entries)
- `examples/minimal/README.md` (README skeleton)
- `docs/adr/0001-template.md`, `docs/adr/0002-health-endpoints.md` (ADR)
- Sunset/deprecation: `examples/good-vs-bad/api.md` (GraphQL `@deprecated`, SemVer)
