# 14 GraphQL

- Relay connections: `edges{cursor,node} + pageInfo{endCursor,hasNextPage}` with opaque cursors. No `offset/limit`. Source: https://graphql.org/learn/pagination/
- Evolve one schema: add field, `@deprecated(reason:)`, track usage, remove after migration. No `/v2` forks, no silent removals. Sources: https://graphql.org/learn/governance-versioning/, https://graphql.org/learn/best-practices/
- Check: `findBreakingChanges` / schema breaking gate in CI. Waivers: `docs/waivers.md`.

## Examples
- `examples/good-vs-bad/api.md` (connections, deprecation)
