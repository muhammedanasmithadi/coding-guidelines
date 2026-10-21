# Migration for legacy code

New repos adopt strict gates day one. Legacy repos use baseline + ratchet.

## Steps

1. Generate baseline: `scripts/make-baseline.sh` writes current violations to `waivers/baseline.<tool>.json` (ruff) and `waivers/baseline.check-tree.json` (tree gate).
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

## 0.19.0 adopters

New blocking gates: docstrings, JS/TS block comments, ADR fields, language enforce configs.

1. Delete module and function docstrings; move the purpose to the script index in `docs/tooling.md` or the module README.
2. Keep only machine directives (`noqa`, `#[allow]`, `@Suppress`, `//nolint`) and doc comments a named tool requires (Go godoc).
3. Copy each existing ADR into `docs/adr/NNNN-slug.md` with `Status`, `Context`, `Options`, `Decision`, `Consequences`; add `Options` if it was missing.
4. Give every language doc a non-empty `enforce/<language>/` config and reference it from the doc.
5. Existing violations go through the baseline + ratchet path above; new violations block. `scripts/check_tree.py` findings ratchet through `waivers/baseline.check-tree.json`; a baselined finding is reported as `baseline:` and a new one fails.

Sources: Expand-contract / Parallel Change (Fowler), docs/adr/0008-rationale-routing.md

## Examples

- `waivers/baseline.<tool>.json` (ratchet input)
- `scripts/make-baseline.sh` (generator)
- `docs/tech-debt.md` (burn-down tracking)
- `docs/adoption.md` (done checklist for the migrated repo)
