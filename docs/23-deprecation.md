# 23 Deprecation

- Announce 2 versions ahead. Emit `Sunset` + `Deprecation` headers with successor link. Remove after window.
- GraphQL: `@deprecated(reason:)` with usage tracking. Shared libs: `@deprecated` + MAJOR removal.
- Check: breaking-change gate (`oasdiff`/`buf`) fails unannounced removals. Waivers: `docs/waivers.md` (shorten window only with consumer sign-off).

Sources: IETF Sunset https://datatracker.ietf.org/doc/html/rfc8594

## Examples

- `examples/good-vs-bad/api.md` (GraphQL `@deprecated`, SemVer)
