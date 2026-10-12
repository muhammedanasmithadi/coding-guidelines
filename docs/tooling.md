# Tooling

Single source of truth per toolchain — no separate pins file (a versions list
duplicates the lockfiles and rots; deleted in v0.11):

- JS: exact pins in `package.json` + `package-lock.json` (committed).
- Python CI: exact pins in `requirements-ci.txt` (monitored by Dependabot pip).
- Runtimes: `.python-version` (mise, setup-python `version-file`) and `.nvmrc`
  (mise, setup-node `node-version-file`). CI reads the same files developers use.
- Gitleaks tracks its GitHub Action major (`gitleaks/gitleaks-action@v3`); semgrep has no CI step yet (see `checks/security-gates.md`).
- Link checking runs only in CI (`lycheeverse/lychee-action`): the pre-commit lychee hook needs a local binary and duplicates the CI gate.
- Local speed: `prek` (Rust pre-commit replacement, verified green on this repo) is the recommended local runner. CI stays on `pre-commit/action` until the pilot concludes.

## Examples

- `package.json`, `requirements-ci.txt` (pins under audit), `scripts/check-drift.sh`, `scripts/bootstrap.sh`
