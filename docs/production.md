# Production

## Health
- Expose `/healthz`, `/readyz`. K8s probes: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
- Drain on SIGTERM. Respect `terminationGracePeriodSeconds`.

## Release
- Flag features (OpenFeature). Roll canary/blue-green. Auto-rollback on SLO burn.
- Define SLOs/SLIs + error budgets. Source: https://sre.google/workbook/table-of-contents/

## Data/Privacy
- Classify PII. Minimize. Set retention/deletion. Test restore (RPO/RTO).
- Run k6 https://k6.io/ on critical paths. Budget p95/p99 + bundle size + DB query count.
