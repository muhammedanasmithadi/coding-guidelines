# Review throughput

- PRs <400 LOC soft cap (bot comments above). Stacked diffs for large work (`gh stack`/`spr`).
- `quality.yml` splits into parallel `lint`/`typecheck`/`security` jobs with caching + `concurrency:` cancel.
- Merge queue on main. Auto-merge `chore(deps)` when green.
- Small, reviewable, revertible beats large and blocked.

## Examples

- `.github/workflows/quality.yml`, `.github/pull_request_template.md`
