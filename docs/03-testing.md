# 03 Testing

TEAM CHOICE: 80% floor is local policy, not a tool default.

- Cover 80% lines + branches. Gate: `--fail-under=80`. Patch coverage must not drop.
- Write property tests for parsers/math/state machines: Hypothesis https://hypothesis.works/, fast-check https://github.com/dubzzz/fast-check.
- Fuzz every untrusted parser/decoder/serializer and public endpoint shape: Python `atheris`, Go `go test -fuzz`, JS `fast-check` (arbitrary bytes), Rust `cargo fuzz`.
- Contract tests across services: Pact https://pact.io/ (or schema conformance) blocks breaking responses.
- E2E only for critical user journeys; deterministic seeds and isolated fixtures (`jest --runInBand --detectOpenHandles`). Browser E2E: Playwright with traced failures and hermetic test data.
- Quarantine flaky: `pytest -m "not quarantine"` (register `quarantine` mark), `go test -shuffle=on -count=3`, `jest --runInBand --detectOpenHandles`.
- Require mutation report on critical paths: Stryker https://stryker-mutator.io/ for JS/TS/Java/C#, `mutmut` for Python, `cargo-mutants` for Rust; gate high >=80.
- No test hits network/disk/clock without fake. Inject clock, seed RNG.
- Test behavior, not implementation: call the code as users do and assert literal expected values. Delete tests that pass when every import returns `undefined`.
- Sequence work into verifiable units: before/after bracket each change and run the check before the next.
- Prove it works: verify the real artifact, not a proxy or "it compiles"; script the check when possible.
- Golden/snapshot tests update only in a dedicated PR with reviewed diff; never auto-accept in CI.
- Mutation score ≥80 on critical paths; block drops (`Stryker` defaults high:80 low:60 break:null; mutation below high fails).
- Flaky test gets quarantined with owner + expiry; no retry-loop masking in CI config.
- Verify adoption with the project's own runner (Django evidence: bare `DiscoverRunner` fails a test that `runtests.py` passes — harness fidelity decides "no regression").

## Test quality (anti-slop)

- One behavior per test; title names the observable outcome (`test_expired_checkout_rejected`), not the function (`test_checkout`).
- Every test has at least one assertion on real observable state. No assertion-free test counts toward coverage.
- No tautological assertions: `assert True`, `x == x`, or `assert result is not None` as the only check. `B011`, `PT018`, and mutation runs catch vacuity.
- A mock call assertion is support, not proof: add at least one assertion on produced state or returned data.
- Derive edges from input partitions and boundary values; do not paste the happy path 10 times.
- Kill surviving mutants on touched code; an un-killed mutant means the edge the test misses.
- Quarantine flaky tests with owner and expiry; no `pytest.skip`, no commented asserts, no retry-loop masking.
- Tests are independent: no execution-order or shared-global-state dependence.
- Snapshot and golden updates only in a dedicated reviewed PR; never auto-accept.
- Test behavior as users see it; tests pass only when the behavior holds, including when every import returns `undefined` if the design is wrong.

Sources: https://hypothesis.works/, https://github.com/dubzzz/fast-check., https://pact.io/, https://stryker-mutator.io/, https://arxiv.org/abs/2406.10279

Commands:

- Python: `coverage run -m pytest && coverage report --fail-under=80`
- TS: `jest --coverage --coverageThreshold='{"global":{"lines":80,"branches":80}}'`
- Go: `go test -coverprofile=cover.out ./... && go tool cover -func=cover.out | awk '/total:/{exit ($3+0<80)}'`

## Examples

- `examples/good-vs-bad/python.md` §9 (fixtures, Hypothesis)
- `examples/good-vs-bad/typescript.md` §7 (vitest/fast-check)
- `examples/good-vs-bad/testing-gaps.md` (quarantine, fake clock, mutation)
