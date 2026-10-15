# Tooling

Single source of truth per toolchain — no separate pins file (a versions list
duplicates the lockfiles and rots; deleted in v0.11):

- JS: exact pins in `package.json` + `package-lock.json` (committed).
- Python CI: exact pins in `requirements-ci.txt` (monitored by Dependabot pip).
- Runtimes: `.python-version` (mise, setup-python `version-file`) and `.nvmrc`
  (mise, setup-node `node-version-file`). Track the latest Python stable release and
  the active Node.js LTS major, and auto-bump patch releases weekly via
  `.github/workflows/runtime-bump.yml`. CI reads the same files developers use.
- Gitleaks tracks its GitHub Action major (`gitleaks/gitleaks-action@v3`); semgrep runs `p/default` at ERROR severity on `scripts/` in CI (see `checks/security-gates.md`).
- Shell scripts lint with `shellcheck`, Dockerfiles with `hadolint`, Terraform with `tflint`, Kubernetes manifests with `kubeconform`, container images with `trivy`.
- Link checking runs only in CI (`lycheeverse/lychee-action`): the pre-commit lychee hook needs a local binary and duplicates the CI gate.
- Local speed: `prek` (Rust pre-commit replacement) is the recommended local runner: measured 8.4s vs 17.6s for `pre-commit` on a warm cache, identical 11/11 hooks green. CI stays on `pre-commit/action` (stability over seconds on an already-fast pipeline).
- Tools are reference implementations, never mandates: principles are normative, any tool enforcing the stated principle conforms. Re-scan the landscape quarterly (`scripts/check-freshness.sh`, `docs/audit.md`) before bumping majors; record swaps as ADRs when a gate changes.
- Adoption-level checks (`oasdiff`, `buf`, `squawk`, `hadolint`, `tflint`, `kubeconform`, `trivy`, `promtool`, `axe`/Lighthouse, Playwright, k6, Pact, CycloneDX) are not run in this repo; adopters map them to their scopes and budgets.

Sources: docs/adr/0004-ts7-via-oxlint-type-aware.md, scripts/check-freshness.sh

## Examples

- `package.json`, `requirements-ci.txt` (pins under audit), `scripts/check-drift.sh`, `scripts/bootstrap.sh`
