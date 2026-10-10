# Production — Do vs Avoid

Sources: OTel https://opentelemetry.io/docs/concepts/signals/traces/, K8s probes https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/, OWASP https://owasp.org/www-project-top-ten/, SRE https://sre.google/sre-book/chapters/service-level-objectives/

## Logging

Do: JSON to stdout with `trace_id`, `service`, `level`. Agent ships.
Avoid: `print(f"got {user} {password}")`. unfilterable, leaks secrets. MTTR 10min becomes 6h.

## Tracing

Do: OTel SDK + OTLP + W3C `traceparent` propagation. Sample 10%, 100% on errors.
Avoid: custom `X-Request-ID` in one hop only. p99 jump root cause stays hidden 3 days.

## Metrics

Do: RED per route + USE per node in Prometheus. Alert on SLO burn only.
Avoid: `tail -f | grep ERROR`, avg latency only. Tail regression missed. High-cardinality `user_id` label OOMs Prometheus.

## Timeouts / breaker

Do:
```python
client = httpx.AsyncClient(timeout=httpx.Timeout(0.8, connect=0.2))
# retry 3x timeout/connect only, full jitter, breaker 20 fails/30s, Idempotency-Key on POST
```

Avoid: `while True: requests.get(url)` no timeout. Fixed 1s retry x10. Retry on 4xx charge. Causes retry storm, cascade.

## Probes

Do: `/livez` (no deps) + `/readyz` (checks DB) + `startupProbe` for slow boot.
Avoid: none, or single `/health` hitting DB. No readiness sends traffic to warming pods (30% 502s). Liveness on DB restarts fleet on DB blip.

## Shutdown

Do: `SIGTERM` -> stop accept, drain 25s, close pools. `terminationGracePeriodSeconds: 30` + `preStop sleep 5`.
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

Do:
```dockerfile
FROM python:3.12.3-slim-bookworm@sha256:<digest>
RUN useradd -r -u 65532 app
USER 65532:65532
```

Avoid: `FROM python:latest` as root. RCE runs as host root. `latest` drifts CVEs.

## K8s

Do: `requests 100m/128Mi`, `limits 500m/512Mi`, probes, `PDB minAvailable: 2`, HPA on p95/RPS.
Avoid: no limits/probes, single replica. Noisy neighbor OOMs node. Drain takes full outage.

## Flags / canary

Do: OpenFeature flag + canary 1%->10%->100% + auto-rollback on burn. Kill-switch per flag.
Avoid: Friday big-bang 100%. 100% blast radius, manual rollback, data repair 6h.

## SLOs

Do: 99.9%/28d = 43min budget. Fast-burn 14.4x/1h page, slow-burn 6x/6h ticket. Freeze deploys when exhausted.
Avoid: alert `CPU>80%`, any 500 to `#alerts`. 300/day spam, real page ignored.
