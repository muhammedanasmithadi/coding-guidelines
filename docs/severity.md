# Severity

Each check declares `severity` and `stage`:

- `blocking`: fails merge.
- `warning`: posts PR comment, passes.
- `advisory`: runs nightly, files issue.

Stages: `pilot` (2-4 weeks as warning) -> `enforcing` (blocking).

New rules start pilot. Promote with data: false-positive rate <5%, pilot repos green.

## Examples

- `docs/audit.md` (promotion review)
- `docs/adr/` (MAJOR changes recorded)
