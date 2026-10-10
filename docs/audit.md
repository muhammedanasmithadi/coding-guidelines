# Audit (quarterly)

Owner rotates. Checklist:

- [ ] Waivers reviewed: expired removed, active still valid.
- [ ] False-positive rate per rule checked. Noisy rules demoted.
- [ ] Tool versions bumped (`enforce/versions.lock`), examples CI green.
- [ ] Coverage/complexity thresholds still fit (80%, CC<15).
- [ ] Examples run against current configs.
- [ ] File audit issue from `.github/ISSUE_TEMPLATE/audit.md`.

Record outcome as ADR if a gate changes severity.

## Examples
- `enforce/versions.lock` (tool versions under audit)
- `.github/ISSUE_TEMPLATE/audit.md` (quarterly record)
- `docs/adr/` (outcome of gate changes)
