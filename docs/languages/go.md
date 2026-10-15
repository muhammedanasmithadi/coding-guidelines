# Go

Sources: Effective Go https://go.dev/doc/effective_go, `gofmt` https://pkg.go.dev/cmd/gofmt

## Enforce

- Format: `gofmt -l .` must print nothing.
- Vet + lint: `go vet ./...`, `golangci-lint run` (covers `govet`, `staticcheck`, `ineffassign`, `revive`, plus `errcheck`, `gosec`).
- Test: `go test -race -coverprofile=cover.out ./... && go tool cover -func=cover.out | awk '/total:/{exit ($3+0<80)}'` (80 = TEAM CHOICE).
- Flaky: `go test -shuffle=on -count=3 ./...`.

## Rules

- `gofmt` tabs, no manual alignment. Godoc on exported names.
- Small interfaces (`io.Reader` style). Accept interfaces, return structs.
- `context.Context` first arg on I/O. No goroutine leaks: bound pools, never unbounded `go f()` in a loop.

Other languages (Rust/Java/C#): deferred. Go pilots next after Python/TS.

## Examples

- `checks/coverage-thresholds.md` (Go cover gate)
- Waivers: `docs/waivers.md`
