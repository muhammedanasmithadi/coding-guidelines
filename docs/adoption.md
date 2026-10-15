# Adoption: definition of done

A repo has adopted these guidelines when every item below verifies green.
Run the commands; no item is satisfied by assertion.

## Two ways to adopt

**By URL (recommended):** reference the reusable workflow — no file copying, no
drift, version pinned by tag:

```yaml
jobs:
  guidelines:
    uses: muhammedanasmithadi/coding-guidelines/.github/workflows/reusable.yml@v0.18.0
    with:
      guidelines-ref: v0.18.0
```

The tag in `uses:` and `guidelines-ref` must match. Local hooks still need the
4 dotfiles + `enforce/` copied (see `examples/minimal/README.md`) — hook
entries use paths relative to the repo root, so they cannot run from a URL.

**By copy:** follow `examples/minimal/README.md`, proven by `scripts/verify-starter.sh`.

## Done checklist

- [ ] Local gates green: `pre-commit run --all-files` (or `prek run --all-files`).
- [ ] CI `quality` green on main, including coverage floor with no drop vs main.
- [ ] `python3 scripts/check_waivers.py` prints `waivers ok` — every exception is filed in `waivers/active.yml` with owner + expiry ≤90d, or the file is absent.
- [ ] `python3 scripts/check_tree.py` prints `tree ok` — no orphans, no dangling refs, every doc has examples.
- [ ] Complexity: no new CC>15/L>200 functions vs `waivers/baseline.*` (or the baseline burn-down is on track per `docs/migration.md`).
- [ ] Secrets + deps: secret scan clean, `pip-audit --strict` / `npm audit --audit-level=high` clean, lockfiles committed.
- [ ] Version recorded: the adopted tag (`vX.Y.Z`) noted in the repo (README or adoption record) so drift is detectable via `scripts/check-drift.sh`.

## Paths

- Greenfield: all items from day one, no baseline files.
- Legacy: same list, plus a committed baseline and the first burn-down entry. See `docs/migration.md`.
- À la carte (principles-first): each adopted principle maps to an enforcer command above or to a named reviewer check in the PR template. Unmapped principles are not adopted — say so explicitly.

## Examples

- `examples/minimal/` (starter files; `scripts/verify-starter.sh` proves the flow in CI), `docs/migration.md` (baseline flow), `docs/waivers.md` (exception format)
