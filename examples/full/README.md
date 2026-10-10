# Full adopter

Full service example. Copies minimal + adds:

- `openapi.yaml` + `spectral lint` + `oasdiff breaking`
- `migrations/` + `squawk ./migrations/*.sql`
- `Dockerfile` + `hadolint`
- `k8s/` + `kubeconform`
- `src/` with OTel, `/livez` `/readyz`, graceful shutdown
- k6 load test in `tests/load/`

See `docs/production.md` for required endpoints and budgets.
