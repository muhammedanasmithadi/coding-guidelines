# Coverage thresholds

- 80% lines + branches per repo. Patch coverage must not drop vs main.
- Python: `coverage report --fail-under=80`
- TS: jest `coverageThreshold global lines 80 branches 80`
- Go: `go tool cover -func=cover.out` gate 80
- Java: JaCoCo check rule 80

Ratchet: raise 5 points per quarter until 90 on critical services.
