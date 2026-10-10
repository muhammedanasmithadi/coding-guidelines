# Performance budgets

All numbers are TEAM CHOICE per service. Calibrate by load test, do not copy blindly.

- API p95 <300ms, p99 <800ms on critical paths. k6 https://k6.io/ runs in CI nightly.
- Web bundle <200KB initial. Fail on +10% regression.
- DB: <5 queries per request, no N+1. Explain on new query.
- Complexity: Lizard `CC<15` (upstream default), file <200 LOC (TEAM CHOICE, upstream default 1000).
