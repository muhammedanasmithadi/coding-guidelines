# 24 Infra as code

- Dockerfiles: `hadolint` for Dockerfile lint, non-root user, pinned base image digest, multi-stage build.
- Terraform/OpenTofu: `tflint` + `terraform fmt` + plan review. No secrets in tfvars.
- Kubernetes: `kubeconform` against pinned schema, resource requests/limits, no `latest` tag, Pod Security Standards restricted.
- Supply chain: SBOM (CycloneDX) + `trivy` image scan, 0 high/critical before deploy.
- Check: `hadolint Dockerfile`, `tflint`, `kubeconform -strict manifests/`, `trivy image --exit-code 1 --severity HIGH,CRITICAL app:tag`, SBOM gate per release.
- Waivers: `docs/waivers.md`.

## Examples

- `examples/full/README.md` (Dockerfile + hadolint, k8s + kubeconform)
- `checks/security-gates.md` (image scan, SBOM)
- `docs/production.md` (probes, drain, SLO)
