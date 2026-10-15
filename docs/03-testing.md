# 03 Testing

TEAM CHOICE: 80% floor is local policy, not a tool default.

- Cover 80% lines + branches. Gate: `--fail-under=80`. Patch coverage must not drop.
- Write property tests for parsers/math/state machines: Hypothesis https://hypothesis.works/, fast-check https://github.com/dubzzz/fast-check.
- Fuzz every untrusted parser/decoder/serializer and public endpoint shape: Python `atheris`, Go `go test -fuzz`, JS `fast-check` (arbitrary bytes), Rust `cargo fuzz`.
- Contract tests across services: Pact https://pact.io/ (or schema conformance) blocks breaking responses.
- E2E only for critical user journeys; deterministic seeds and isolated fixtures (`jest --runInBand --detectOpenHandles`).
- Quarantine flaky: `pytest -m "not quarantine"` (register `quarantine` mark), `go test -shuffle=on -count=3`, `jest --runInBand --detectOpenHandles`.
- Require mutation report on critical paths: Stryker https://stryker-mutator.io/ (defaults high:80 low:60 break:null), cargo-mutants.
- No test hits network/disk/clock without fake. Inject clock, seed RNG.
- Golden/snapshot tests update only in a dedicated PR with reviewed diff; never auto-accept in CI.
- Mutation score ≥80 on critical paths; block drops (`Stryker` defaults high:80 low:60 break:null; mutation below high fails).
- Flaky test gets quarantined with owner + expiry; no retry-loop masking in CI config.
- Verify adoption with the project's own runner (Django evidence: bare `DiscoverRunner` fails a test that `runtests.py` passes — harness fidelity decides "no regression").

Commands:

- Python: `coverage run -m pytest && coverage report --fail-under=80`
- TS: `jest --coverage --coverageThreshold='{"global":{"lines":80,"branches":80}}'`
- Go: `go test -coverprofile=cover.out ./... && go tool cover -func=cover.out | awk '/total:/{exit ($3+0<80)}'`

## Examples

- `examples/good-vs-bad/python.md` §9 (fixtures, Hypothesis)
- `examples/good-vs-bad/typescript.md` §7 (vitest/fast-check)
- `examples/good-vs-bad/testing-gaps.md` (quarantine, fake clock, mutation)
