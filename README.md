# coding-guidelines

Docs + enforcing configs + verified CI. Each rule maps to a command. CI blocks merge on failure.

Principles are normative; tool configs are a reference implementation. Libraries
are cited as conforming examples, never mandates: any tool that enforces the
stated principle conforms. A rule names a specific library only when no
principle-level check exists.

## Use

1. Read `docs/onboarding.md`.
2. Copy `enforce/` + `checks/` + `.github/workflows/quality.yml` into your repo.
3. Run `pre-commit run --all-files`. Fix failures. Push. CI runs the same commands.
4. Pin version: reference this repo by tag `vX.Y.Z` (see `VERSION`, `CHANGELOG.md`).
5. Declare done per `docs/adoption.md` — every item verifies with a command.

## Layout

- `docs/` — rules. `docs/languages/` — per-language appendices.
- `enforce/` — `.editorconfig`, `pre-commit`, formatter/linter configs, pinned versions.
- `checks/` — thresholds that fail CI.
- `examples/` — minimal/full adopters + good-vs-bad diffs. CI tests them against current configs.
- `waivers/` — temporary exceptions with expiry. CI fails on expired waiver.

## Scripts

- `scripts/bootstrap.sh` — one-command golden path: toolchain + hooks + local gates.
- `scripts/check-drift.sh <tag>` — diffs local `enforce/` + `checks/` against a released tag (advisory).
- `scripts/check-freshness.sh` — reports pinned-vs-latest drift (advisory).
- `scripts/run-codemod.sh <sgconfig.yml> [path]` — ast-grep codemod scan across adopters.
- `scripts/make-baseline.sh` — writes current violations to `waivers/baseline.<tool>.json` for ratchet mode.
- `scripts/check_waivers.py`, `scripts/check_tree.py` — CI gates (also run via `make check`).
- `scripts/verify-starter.sh` — end-to-end adoption proof (scaffolds a temp repo per `examples/minimal/README.md`, runs the gates).

## Versioning

MAJOR = breaking gate. MINOR = new check. PATCH = fix/clarify. See `CHANGELOG.md`.

## Licenses

Code/configs/examples: Apache-2.0. Docs: CC-BY-4.0. See `LICENSE`.
