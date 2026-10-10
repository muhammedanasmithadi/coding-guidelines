# 15 Versioning

- SemVer `MAJOR.MINOR.PATCH`: break → MAJOR, add compat → MINOR, fix → PATCH. Never mutate a release. Source: https://semver.org/
- APIs under `/v1`. Changelog per release (Keep a Changelog). Shared libs follow the same rule; export removal is MAJOR.
- Check: `oasdiff`/`buf breaking` + changelog gate. Waivers: `docs/waivers.md` (breaking-change RFC: `docs/rollout.md`).

## Examples
- `examples/good-vs-bad/api.md` (SemVer), `commits.md` (changelog entries)
