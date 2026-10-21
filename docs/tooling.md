# Tooling

Single source of truth per toolchain — no separate pins file (a versions list
duplicates the lockfiles and rots; deleted in v0.11):

- JS: exact pins in `package.json` + `package-lock.json` (committed).
- Python CI: exact pins in `requirements-ci.txt` (monitored by Dependabot pip).
- Runtimes: `.python-version` (mise, setup-python `version-file`) and `.nvmrc`
  (mise, setup-node `version-file`). Track the active Python supported stable
  series and the active Node.js LTS major, auto-bump patch releases weekly through
  `.github/workflows/runtime-bump.yml`, and change either major only through an ADR
  (`docs/adr/0006-runtime-lts-majors.md`) when the current series nears end-of-life
  (`docs/adr/0007-runtime-major-upgrade-policy.md`). `enforce/runtime-baseline.yml`
  holds the tracked series and the ADR that authorized each; `scripts/check_tree.py`
  fails when a pin leaves its series. CI reads the same files developers use.
- Gitleaks tracks its GitHub Action major (`gitleaks/gitleaks-action@v3`); semgrep runs `p/default` at ERROR severity on `scripts/` in CI (see `checks/security-gates.md`).
- Shell scripts lint with `shellcheck`, Dockerfiles with `hadolint`, Terraform with `tflint`, Kubernetes manifests with `kubeconform`, container images with `trivy`.
- Link checking runs only in CI (`lycheeverse/lychee-action`): the pre-commit lychee hook needs a local binary and duplicates the CI gate.
- Local speed: `prek` (Rust pre-commit replacement) is the recommended local runner: measured 8.4s vs 17.6s on a warm cache, identical 11/11 hooks green. CI stays on `pre-commit/action` (stability over seconds on an already-fast pipeline).
- Tools are reference implementations, never mandates: principles are normative, any tool enforcing the stated principle conforms. Re-scan the landscape quarterly (`scripts/check-freshness.sh`, `docs/audit.md`) before bumping majors; record swaps as ADRs when a gate changes.
- Adoption-level checks (`oasdiff`, `buf`, `squawk`, `hadolint`, `tflint`, `kubeconform`, `trivy`, `promtool`, `axe`/Lighthouse, Playwright, k6, Pact, CycloneDX) are not run in this repo; adopters map them to their scopes and budgets.

## Repo scripts

Each script states its purpose here, not in a docstring (`docs/01-principles.md`).

| Script                              | Purpose                                                                                                   |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `scripts/agent-context.py`          | Print the curated docs/checks for a task type from `agent-context-map.yml`.                               |
| `scripts/ai_docs_draft.py`          | Open a draft PR with AI-proposed guideline improvements (optional).                                       |
| `scripts/bump-runtime-versions.py`  | Bump `.python-version` and `.nvmrc` within their pinned majors.                                           |
| `scripts/check_action_pins.py`      | Report workflow actions that are not pinned to a commit SHA.                                              |
| `scripts/check_alert_runbooks.py`   | Ensure alerting rules reference a runbook when present.                                                   |
| `scripts/check_cardinality.py`      | Fail when forbidden high-cardinality labels appear in metric code.                                        |
| `scripts/check_changelog.py`        | Fail when docs or checks change without a CHANGELOG entry.                                                |
| `scripts/check_decision_note.py`    | Fail when a rule-changing PR carries no `Decision:` or `Rationale:` note.                                 |
| `scripts/check-comments.sh`         | Report comments in Rust/Kotlin/C/Go sources (advisory).                                                   |
| `scripts/check_import_cycles.py`    | Fail when Python modules import each other in a cycle.                                                    |
| `scripts/check_layer_boundaries.py` | Fail when a module imports from a disallowed architectural layer.                                         |
| `scripts/check_mutation.py`         | Run mutation testing when `mutmut` is available (advisory).                                               |
| `scripts/check_no_any.py`           | Fail when a function boundary is typed as bare `Any`.                                                     |
| `scripts/check_openapi_breaking.py` | Run `oasdiff` breaking-change check when a baseline spec exists.                                          |
| `scripts/check_osv.py`              | Run `osv-scanner` when installed (advisory).                                                              |
| `scripts/check_perf_budgets.py`     | Validate a performance-budgets config when present.                                                       |
| `scripts/check_tree.py`             | Fail CI when repo hygiene slips: NULs, empties, version drift, orphaned examples, docstrings, ADR fields. |
| `scripts/check_version_drift.py`    | Fail when duplicated tool pins drift apart.                                                               |
| `scripts/check_waivers.py`          | Fail CI on expired or over-long waivers in `waivers/active.yml`.                                          |
| `scripts/digest_feedback.py`        | Digest open standard-feedback issues into a summary issue.                                                |
| `scripts/pin_actions.py`            | Pin GitHub Actions to commit SHAs (run once, then keep tags in release notes).                            |
| `scripts/bootstrap.sh`              | One-command golden path: toolchain, hooks, local gates.                                                   |
| `scripts/check-drift.sh`            | Diff local `enforce/` + `checks/` against a released tag (advisory).                                      |
| `scripts/check-freshness.sh`        | Report pinned-vs-latest tool drift (advisory).                                                            |
| `scripts/make-baseline.sh`          | Write current violations to `waivers/baseline.<tool>.json` for ratchet mode.                              |
| `scripts/run-codemod.sh`            | Run an ast-grep codemod scan across adopters.                                                             |
| `scripts/verify-starter.sh`         | End-to-end adoption proof: scaffolds a temp repo and runs the gates.                                      |

Sources: docs/adr/0004-ts7-via-oxlint-type-aware.md, docs/adr/0006-runtime-lts-majors.md, scripts/check-freshness.sh

## Examples

- `package.json`, `requirements-ci.txt` (pins under audit), `scripts/check-drift.sh`, `scripts/bootstrap.sh`
