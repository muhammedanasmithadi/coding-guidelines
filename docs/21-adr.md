# 21 ADR

- One short record per decision: context, options, decision, consequences. Numbered, immutable, superseded never edited.
- Required for MAJOR gate changes, breaking APIs, and topology choices.
- ADRs are decision records, not guides: exempt from the `## Examples` rule in `scripts/check_tree.py`.
- Check: ADR present in rule PR (`CONTRIBUTING.md` checklist). Waivers: N/A (process doc).

Sources: Nygard ADR https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions

## Examples

- `docs/adr/0001-template.md`, `docs/adr/0002-health-endpoints.md`, `docs/adr/0003-supported-languages.md`
