# Performance budgets

All numbers are TEAM CHOICE per service. Calibrate by load test, do not copy blindly.

- API p95 <300ms, p99 <800ms on critical paths. k6 https://k6.io/ runs in CI nightly.
- Web bundle <200KB initial. Fail on +10% regression.
- Core Web Vitals (Lighthouse): LCP <2.5s, INP <200ms, CLS <0.1 on mobile, gated in CI.
- Profiling: `py-spy`, `node --prof`/`0x`, or `pprof` for hot paths before a perf PR merges.
- DB: <5 queries per request, no N+1. Explain on new query.
- Complexity: Lizard `CC<15` (upstream default), file <200 LOC (TEAM CHOICE, upstream default 1000).
- Real-time: connection p95 handshake <100ms, message fanout <50ms, memory growth <5% over soak.
