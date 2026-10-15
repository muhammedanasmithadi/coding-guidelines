# Migration for legacy code

New repos adopt strict gates day one. Legacy repos use baseline + ratchet.

## Steps

1. Generate baseline: `scripts/make-baseline.sh` writes current violations to `waivers/baseline.<tool>.json`.
2. CI blocks new violations only. Old violations burn down.
3. Set burn-down SLO: e.g. reduce baseline 10% per sprint.
4. Remove baseline entries as code is fixed. Delete baseline file at zero.
5. No new repo adopts with a baseline without owner approval.

## Rules

- Baseline files live in `waivers/`, carry owner + date.
- No edit to baseline without PR + CODEOWNER review.
- Migrate callers then delete legacy APIs in one wave; no long-lived adapters.
- Outcome-oriented: converge on the target architecture, not smooth intermediate compatibility states.
- Ratchet never loosens: thresholds move one direction (stricter).

## Examples

- `waivers/baseline.<tool>.json` (ratchet input)
- `scripts/make-baseline.sh` (generator)
- `docs/tech-debt.md` (burn-down tracking)
- `docs/adoption.md` (done checklist for the migrated repo)
