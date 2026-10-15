# Context (ubiquitous language)

- **Rule**: normative requirement, named and testable.
- **Gate**: command in CI that fails on violation.
- **Check**: threshold (coverage, complexity, bundle size).
- **Waiver**: temporary numbered exception with owner, reason, expiry; tracked in `waivers/active.yml`.
- **Baseline/ratchet**: accepted violations only decrease over time; no baseline without owner approval.
- **ADR**: numbered decision record, immutable once accepted; supersede by new ADR.
- **Tier**: standard (default) vs mission-critical service level.
- **Adopter**: repository consuming these guidelines.
- **Source**: authoritative citation behind a rule.
