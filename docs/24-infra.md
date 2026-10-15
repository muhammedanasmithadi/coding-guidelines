# 24 Infra as code

- Dockerfiles: lint (hadolint or equivalent), non-root user, pinned base image digest, multi-stage build.
- Terraform/OpenTofu: lint + format + plan review (tflint or equivalent). No secrets in tfvars.
- Kubernetes: schema validation (kubeconform or equivalent), pinned schema, resource requests/limits (calibrated CPU/memory), no `latest` tag, Pod Security Standards restricted.
- Supply chain: SBOM (CycloneDX or SPDX) + container image scan (trivy or equivalent), 0 high/critical before deploy.
- Check: image/container lint, IaC lint+fmt+plan, manifest schema validation, image scan with 0 high/critical, and SBOM gate per release.
- Waivers: `docs/waivers.md`.

Sources: Docker docs https://docs.docker.com/, Kubernetes docs https://kubernetes.io/docs/, Terraform docs https://developer.hashicorp.com/terraform

## Examples

- `examples/good-vs-bad/ai-slop.md` (agent failure modes in this area)

- `examples/full/README.md` (Dockerfile + hadolint, k8s + kubeconform)
- `checks/security-gates.md` (image scan, SBOM)
- `docs/production.md` (probes, drain, SLO)
