# 29 Reproducible builds and provenance

- Lockfiles committed and checked; byte-reproducible builds for release artifacts; no floating versions in CI.
- Hermetic builds: pin base images by digest, toolchain versions by `.python-version`/`.nvmrc`, and container dependencies by lockfile.
- Provenance: SLSA ≥2 for releases, signed artifacts (Sigstore/cosign), SBOM (CycloneDX) published per release.
- Build from a clean checkout in CI; no ambient machine state; cache keys include all inputs.
- Third-party actions pinned by SHA; dependency updates reviewed, not auto-merged silently for critical packages.
- Check: `docker build --no-cache` smoke test, `cosign verify` (or equivalent), `slsa-verifier`, SBOM (CycloneDX or SPDX), reproducibility diff, and pinned action SHA scan.
- Sources: SLSA https://slsa.dev/, Sigstore https://www.sigstore.dev/, Reproducible Builds https://reproducible-builds.org/
- Waivers: `docs/waivers.md`.

## Examples

- `docs/tooling.md` (single source of truth for pins)
- `checks/security-gates.md` (SBOM, scans)
- `.github/workflows/release.yml` (bundle + release)
