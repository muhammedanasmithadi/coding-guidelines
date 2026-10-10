# Contributing

## Flow

1. Open proposal issue: state problem, show false-positive rate, include before/after example.
2. Add ADR in `docs/adr/` for MAJOR gate changes.
3. Pilot on 1-2 repos for 2-4 weeks as `warning`. Collect data.
4. Promote to `blocking` with version bump (MAJOR/MINOR) + CHANGELOG entry.

## Requirements for a rule PR

- Problem statement with incident or review cost.
- Enforcer command that fails CI.
- Example in `examples/good-vs-bad/`.
- Rollout plan: pilot scope, migration note, waiver path.

Docs use present tense, active voice. Cite authoritative source per rule.
