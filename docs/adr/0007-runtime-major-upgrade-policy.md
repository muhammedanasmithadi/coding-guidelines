# ADR 0007: Runtime major upgrade policy

- Status: accepted
- Context: Patch bumps are automated, but major runtime moves can break linters, type checkers, SDKs, and adopters.
- Decision: Change a runtime major only near its predecessor's end-of-life, after a temporary compatibility branch proves all gates pass, or when a security boundary requires it.
- Consequences: The automated patch job stays within the active series; every major upgrade gets a separate ADR or migration note, and adopters observe the change as a major guideline release.
