# Production — Do vs Avoid

Sources: OTel https://opentelemetry.io/docs/concepts/signals/traces/, K8s probes https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/, OWASP https://owasp.org/www-project-top-ten/, SRE https://sre.google/sre-book/chapters/service-level-objectives/

## Logging

Do: JSON to stdout with `trace_id`, `service`, `level`. Agent ships.
Avoid: `print(f"got {user} {password}")`. unfilterable, leaks secrets. MTTR 10min becomes 6h.

## Tracing

Do: OTel SDK + OTLP + W3C `traceparent` propagation. Sample 10% head (TEAM CHOICE), 100% on errors via tail sampler/Collector.
Avoid: custom `X-Request-ID` in one hop only. p99 jump root cause stays hidden 3 days.

## Metrics

Do: RED per route + USE per node in Prometheus (TEAM CHOICE cardinality). Alert on SLO burn only.
Avoid: `tail -f | grep ERROR`, avg latency only. Tail regression missed. High-cardinality `user_id` label OOMs Prometheus.

## Timeouts / breaker

Do (TEAM CHOICE numbers, calibrate per downstream p99):
```python
client = httpx.AsyncClient(timeout=httpx.Timeout(0.8, connect=0.2))
# retry 3x timeout/connect only, full jitter, breaker 20 fails/30s, Idempotency-Key on POST
# (Microsoft/Azure term: Repeatability-Request-ID; Stripe term: Idempotency-Key)
```

Avoid: `while True: requests.get(url)` no timeout. Fixed 1s retry x10. Retry on 4xx charge. Causes retry storm, cascade.

## Probes

Do: `/livez` (no deps) + `/readyz` (checks DB) + `startupProbe` for slow boot.
Avoid: none, or single `/health` hitting DB. No readiness sends traffic to warming pods (30% 502s). Liveness on DB restarts fleet on DB blip.

## Shutdown

Do: `SIGTERM` -> stop accept, drain 25s, close pools. `terminationGracePeriodSeconds: 30` (default) + `preStop sleep 5` (TEAM CHOICE).
Avoid: ignore `SIGTERM`, grace 0. Every deploy drops in-flight checkouts.

## Secrets

Do: ExternalSecrets from Vault, env-injected, rotation, gitleaks in CI.
Avoid: `DB_PASSWORD="prod123"` in code/`.env`/Docker `ENV`. Leaks in git + image layers. Miners hit in minutes.

## Auth

Do: IdP JWT RS256 via JWKS, validate `iss/aud/exp`, RBAC deny-by-default per object.
Avoid: `md5(password)`, JWT `alg:none`, `if header[X-User]==admin`. Priv-esc, PII dump.

## Injection

Do:
```python
db.execute(text("SELECT * FROM orders WHERE id=:c"), {"c": cid})
```

Avoid:
```python
query = f"SELECT * FROM users WHERE name='{name}'"  # SQLi
os.system(f"convert {upload} out.png")  # RCE
```

## Dockerfile

Do (tag + UID are TEAM CHOICE; replace `<digest>` with real sha256, never ship literally):
```dockerfile
FROM python:3.12.3-slim-bookworm@sha256:<digest>
RUN useradd -r -u 65532 app
USER 65532:65532
```

Avoid: `FROM python:latest` as root. RCE runs as host root. `latest` drifts CVEs.

## K8s

Do (numbers are TEAM CHOICE per workload, load-test them): `requests 100m/128Mi`, `limits 500m/512Mi`, probes, `PDB minAvailable: 2` (needs replicas >=3), HPA on p95/RPS via Prometheus Adapter custom metric (not native).
Avoid: no limits/probes, single replica. Noisy neighbor OOMs node. Drain takes full outage.

## Flags / canary

Do: OpenFeature flag + canary 5%->25%->100% (single TEAM CHOICE standard) + auto-rollback on burn. Kill-switch per flag.
Avoid: Friday big-bang 100%. 100% blast radius, manual rollback, data repair 6h.

## SLOs

Do: 99.9%/30d ≈ 43min budget (99.9%/28d ≈ 40min). Fast-burn 14.4x/1h page, slow-burn 6x/6h ticket (SRE workbook 30d values). Freeze deploys when exhausted (TEAM CHOICE policy).
Avoid: alert `CPU>80%`, any 500 to `#alerts`. 300/day spam, real page ignored.
