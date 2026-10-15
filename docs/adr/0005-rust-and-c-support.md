# ADR 0005: Add Rust and C language support

- Status: accepted
- Context: a pilot service now requires Rust and C; ADR 0003 deferred them.
- Decision: add `docs/languages/rust.md` and `docs/languages/c.md` with enforce configs (`enforce/rust`, `enforce/c`) and examples.
- Consequences: Rust and C become part of the supported stack for adopting services; Java remains deferred.
