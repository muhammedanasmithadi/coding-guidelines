# Tooling

Single source of truth per toolchain — no separate pins file (a versions list
duplicates the lockfiles and rots; deleted in v0.11):

- JS: exact pins in `package.json` + `package-lock.json` (committed).
- Python CI: exact pins in `requirements-ci.txt` (monitored by Dependabot pip).
- Runtimes: `.python-version` (mise, setup-python `version-file`) and `.nvmrc`
  (mise, setup-node `node-version-file`). CI reads the same files developers use.
- Gitleaks tracks its GitHub Action major (`gitleaks/gitleaks-action@v3`); semgrep has no CI step yet (see `checks/security-gates.md`).
- Shell scripts lint with `shellcheck`, Dockerfiles with `hadolint`, Terraform with `tflint`, Kubernetes manifests with `kubeconform`, container images with `trivy`.
- Link checking runs only in CI (`lycheeverse/lychee-action`): the pre-commit lychee hook needs a local binary and duplicates the CI gate.
- Local speed: `prek` (Rust pre-commit replacement) is the recommended local runner: measured 8.4s vs 17.6s for `pre-commit` on a warm cache, identical 11/11 hooks green. CI stays on `pre-commit/action` (stability over seconds on an already-fast pipeline).

## Examples

- `package.json`, `requirements-ci.txt` (pins under audit), `scripts/check-drift.sh`, `scripts/bootstrap.sh`
