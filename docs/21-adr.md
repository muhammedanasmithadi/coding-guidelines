# 21 ADR

- One short record per decision: context, options, decision, consequences. Numbered and
  immutable; a change lands as a new record that supersedes the old one (`Supersedes:`
  field), and the superseded record flips its Status line to `superseded` with its body
  untouched.
- Bar: two real alternatives and high reversal cost. MAJOR gate changes, breaking APIs,
  and topology choices are sufficient conditions.
- Required fields: `Status`, `Context`, `Options`, `Decision`, `Consequences`, `Enforcement`.
  `Options` names the alternatives considered, or `none — forced by <constraint>`.
  `Enforcement` names the check or gate that enforces the decision, or `review`.
- Link the record to the code it governs: the ADR ID lives in a name or a `rationale:`
  config field, never in a comment.
- A decision a machine can check gets an enforcing artifact carrying its ID; one it
  cannot states `Enforcement: review`.
- ADRs are decision records, not guides: exempt from the `## Examples` rule in
  `scripts/check_tree.py`.
- Check: `scripts/check_tree.py` enforces fields, numbering, the supersede chain, the
  `Enforcement` artifact, and doc links; ADR present in rule PR (`CONTRIBUTING.md`
  checklist); `scripts/check_decision_note.py` fails a rule-changing PR with no
  rationale note. Waivers: N/A (process doc).

Sources: Nygard ADR https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions

## Examples

- `examples/good-vs-bad/ai-slop.md` (agent failure modes + catches)
- `examples/good-vs-bad/comments-and-adrs.md` (comment ban, ADR fields, supersede chain)

- `docs/adr/0001-template.md`, `docs/adr/0008-rationale-routing.md`, `docs/adr/README.md` (index)
