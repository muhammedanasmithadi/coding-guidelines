# ADR 0002: Standardize health endpoints on /livez + /readyz

- Status: accepted
- Context: docs used `/healthz`, examples used `/livez`. Upstream `healthz` is deprecated since K8s 1.16.
- Decision: `/livez` (no deps) + `/readyz` (may check DB) + `startupProbe` for slow boot.
- Consequences: one grep replaces `healthz`; probes distinguish restart vs traffic.
