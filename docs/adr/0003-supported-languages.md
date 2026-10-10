# ADR 0003: Language support — Python/TS/Go now, Rust/Java/C# deferred

- Status: accepted
- Context: coverage checks and principles name-dropped Clippy/Rust and JaCoCo/Java with no language docs or enforce configs.
- Decision: supported = Python, TypeScript, Go (each has `docs/languages/<x>.md` + enforce config + examples). Rust/Java/C# deferred until a pilot service exists; adding one requires language doc + enforce config + examples + CI job in the same PR.
- Consequences: no new Clippy/JaCoCo references without the full set. `docs/01-principles.md` cites only supported toolchains.
