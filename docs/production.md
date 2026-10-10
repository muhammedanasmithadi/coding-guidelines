# Production

## Health
- Expose `/livez` (no deps, restart signal), `/readyz` (can serve, may check DB). Upstream `healthz` is deprecated. K8s probes: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
- Drain on SIGTERM. Respect `terminationGracePeriodSeconds` (default 30).

## Release
- Flag features (OpenFeature) with per-flag kill-switch. Roll canary `5%→25%→100%` (TEAM CHOICE, single standard). Auto-rollback on SLO burn.
- Define SLOs/SLIs + error budgets. Example: 99.9%/30d ≈ 43min budget (99.9%/28d ≈ 40min). Burn: fast 14.4x/1h page, slow 6x/6h ticket (SRE workbook 30d values). HPA on p95 requires Prometheus Adapter custom metric, not native. Source: https://sre.google/workbook/table-of-contents/

## Data/Privacy
- Classify PII. Minimize. Set retention/deletion. Test restore (RPO/RTO).
- Run k6 https://k6.io/ on critical paths. Budget p95/p99 + bundle size + DB query count.
