# 16 Migrations

- Expand-contract (aka Parallel Change): expand (nullable/additive) → batched backfill (`LIMIT 1000`, throttled, kill-switch, off-peak) → switch readers → contract.
- Reversible. No table rewrite without `CONCURRENTLY`. Single-deploy renames are forbidden.
- Check: `squawk ./migrations/*.sql` (https://github.com/sbdchd/squawk). Waivers: `docs/waivers.md`.

## Examples

- `examples/good-vs-bad/api.md` (expand-contract)
