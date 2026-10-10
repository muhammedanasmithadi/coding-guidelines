## Checklist

- [ ] Rule links to enforcer command that fails CI
- [ ] Example added in `examples/good-vs-bad/`
- [ ] Version bumped (`VERSION` + `CHANGELOG.md`)
- [ ] Migration note for existing repos
- [ ] OWASP Top 10 considered for auth/billing/PII changes
- [ ] Waiver needed? Filed in `waivers/active.yml` with expiry
- [ ] Every new check declares its exact file scope (hook `files:`/`types:`, CI paths) — no unbounded scans
- [ ] No comments in code (machine directives only: `noqa`, `pragma`, `type:`, shebang)

## AI-generated code (required if any part is AI-assisted)

- [ ] No placeholder TODOs/skips/gutted tests without linked issues
- [ ] No new dependency without justification (stdlib first)
- [ ] Every behavior claim cites its artifact (test node ID, CI run, command output)
- [ ] APIs verified against installed versions (no hallucinated methods/packages)

## Severity

- [ ] Starts as warning/pilot, or [ ] blocking with data
