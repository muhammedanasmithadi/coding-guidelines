# Contributing

## Flow

1. Open proposal issue: state problem, show false-positive rate, include before/after example.
2. Add ADR in `docs/adr/` when the decision has two real alternatives and high reversal cost — MAJOR gate changes, breaking APIs, and topology choices qualify (`docs/21-adr.md`).
3. Pilot on 1-2 repos for 2-4 weeks as `warning`. Collect data.
4. Promote to `blocking` with version bump (MAJOR/MINOR) + CHANGELOG entry.

## Requirements for a rule PR

- Problem statement with incident or review cost.
- Enforcer command that fails CI.
- Example in `examples/good-vs-bad/`.
- Rollout plan: pilot scope, migration note, waiver path.
- Decision rationale in an ADR, with the ADR ID referenced from a name or a
  `rationale:` config field, never from a comment (`docs/01-principles.md`).
- A `Decision:` or `Rationale:` note in the PR body. `scripts/check_decision_note.py`
  fails the PR without one when it touches `docs/`, `checks/`, `enforce/`, `scripts/`,
  or `.github/workflows/` — and the squash commit keeps the note.

Docs use present tense, active voice. Cite authoritative source per rule.
