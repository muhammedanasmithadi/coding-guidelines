# Tech debt

- Baselines burn down 10%/sprint (TEAM CHOICE). No baseline older than 2 quarters without ADR.
- `TODO(RULE-123)` cites an issue. CI fails on untracked TODO.
- Debt sprint carve-out 15% (TEAM CHOICE). Track per-repo baseline age in `metrics/`.
- Waiver renewal is not debt rollover: expired waivers fail CI (`scripts/check_waivers.py`).

## Examples

- `waivers/active.yml`, `docs/migration.md`, `docs/metrics.md`
