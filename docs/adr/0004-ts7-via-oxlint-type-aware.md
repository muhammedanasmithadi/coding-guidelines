# ADR 0004: TypeScript 7 migration path via oxlint type-aware

- Status: accepted (path proven, awaiting pilot adopter)
- Context: `typescript@7.0.2` native `tsc` typechecks clean, but typescript-eslint hard-crashes at import on TS 7 (ADR-0003 context). The service template cannot migrate until type-aware linting exists for TS 7.
- Decision: when adopting TS 7, replace the template's typescript-eslint `strictTypeChecked` preset with oxlint `--type-aware` (package `oxlint-tsgolint`, verified 7.0.2004) plus individually listed `typescript/*` rules — the preset cannot be consumed, each rule maps 1:1 and is verified on a probe (`no-misused-promises` fires correctly, exit 1).
- Consequences: oxlint parses TS 7 syntax natively (own parser, no TS version coupling); `oxlint-tsgolint` becomes a required dep wherever `--type-aware` runs; rule list must be enumerated, not extended from a preset. Pilot on one adopter repo before changing the template.
