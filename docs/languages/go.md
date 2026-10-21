# Go

Sources: Effective Go https://go.dev/doc/effective_go, `gofmt` https://pkg.go.dev/cmd/gofmt

## Enforce

- Format: `gofmt -l .` must print nothing.
- Vet + lint: `go vet ./...`, `golangci-lint run --config enforce/go/.golangci.yml` (covers `govet`, `staticcheck`, `ineffassign`, `revive`, `godox`, `nolintlint`, plus `errcheck`, `gosec`).
- Test: `go test -race -coverprofile=cover.out ./... && go tool cover -func=cover.out | awk '/total:/{exit ($3+0<80)}'` (80 = TEAM CHOICE).
- Flaky: `go test -shuffle=on -count=3 ./...`.
- Fuzz: `go test -fuzz=Fuzz -fuzztime=30s ./...` for every parser/decoder.

## Rules

- `gofmt` tabs, no manual alignment. Godoc on exported names — the one doc comment a mandated tool requires (`docs/01-principles.md`).
- Small interfaces (`io.Reader` style). Accept interfaces, return structs.
- `context.Context` first arg on I/O. No goroutine leaks: bound pools, never unbounded `go f()` in a loop.

Supported stack per `docs/adr/0005-rust-and-c-support.md`; Java and C# deferred.

## Examples

- `checks/coverage-thresholds.md` (Go cover gate)
- Waivers: `docs/waivers.md`
