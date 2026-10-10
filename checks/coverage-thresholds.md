# Coverage thresholds

TEAM CHOICE: 80% floor is local policy, not a tool default.

- 80% lines + branches per repo. Patch coverage must not drop vs main.
- Python: `coverage report --fail-under=80`
- TS: jest `coverageThreshold global lines 80 branches 80`
- Go: `go test -coverprofile=cover.out ./... && go tool cover -func=cover.out | awk '/total:/{exit ($3+0<80)}'`
- Java: JaCoCo `jacoco:check` with `COVEREDRATIO minimum 0.80` (requires config in pom/build.gradle)

Ratchet: raise 5 points per quarter until 90 on critical services.
