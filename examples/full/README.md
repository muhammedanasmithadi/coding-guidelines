# Full adopter

Full service example. Copies minimal + adds:

- `openapi.yaml` + `spectral lint` + `oasdiff breaking`
- `migrations/` + `squawk lift`
- `Dockerfile` + `hadolint`
- `k8s/` + `kubeconform`
- `src/` with OTel, `/healthz` `/readyz`, graceful shutdown
- k6 load test in `tests/load/`

See `docs/production.md` for required endpoints and budgets.
