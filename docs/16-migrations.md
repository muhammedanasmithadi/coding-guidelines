# 16 Migrations

- Expand-contract (aka Parallel Change): expand (nullable/additive) → batched backfill (`LIMIT 1000`, throttled, kill-switch, off-peak) → switch readers → contract.
- Reversible. No table rewrite without `CONCURRENTLY`. Single-deploy renames are forbidden.
- Check: `squawk ./migrations/*.sql` (https://github.com/sbdchd/squawk), plus a dry-run/rollback drill on a production-like volume. Waivers: `docs/waivers.md`.

Sources: https://github.com/sbdchd/squawk

## Examples

- `examples/good-vs-bad/ai-slop.md` (agent failure modes in this area)

- `examples/good-vs-bad/api.md` (expand-contract)
