# 03 Testing

- Cover 80% lines + branches. Gate: `--fail-under=80`. Patch coverage must not drop.
- Write property tests for parsers/math: Hypothesis https://hypothesis.works/, fast-check https://github.com/dubzzz/fast-check.
- Quarantine flaky: `pytest -m "not quarantine"`, `go test -shuffle=on -count=3`, `jest --runInBand --detectOpenHandles`.
- Require mutation report on critical paths: Stryker https://stryker-mutator.io/, cargo-mutants.
- No test hits network/disk/clock without fake. Inject clock, seed RNG.

Commands:
- Python: `coverage run -m pytest && coverage report --fail-under=80`
- TS: `jest --coverage --coverageThreshold='{"global":{"lines":80,"branches":80}}'`
- Go: `go test -coverprofile=cover.out ./... && go tool cover -func=cover.out`
