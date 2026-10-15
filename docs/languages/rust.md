# Rust

Sources: Rust API guidelines https://rust-lang.github.io/api-guidelines/, `rustfmt` https://rust-lang.github.io/rustfmt/, Clippy https://doc.rust-lang.org/clippy/

## Enforce

- Format: `cargo fmt --check` (rustfmt, 100 columns max; TEAM CHOICE vs upstream 100). Config `enforce/rust/rustfmt.toml`.
- Lint: `cargo clippy --all-targets --all-features -- -D warnings` (Clippy, pedantic + nursery opted in per crate). Config `enforce/rust/clippy.toml`.
- Types/borrow: `cargo build` strict by default; `deny(warnings)` on CI; `clippy::unwrap_used` and `clippy::expect_used` for production paths.
- Test: `cargo test`, `cargo nextest run` for parallel execution.
- Fuzz: `cargo fuzz run` for parsers/decoders.
- Coverage: `cargo llvm-cov --fail-under-lines 80` (80 = TEAM CHOICE).
- Mutation: `cargo mutants` on critical paths.
- Security: `cargo audit --deny warnings`, `cargo deny check`, `cargo miri test` for crates with unsafe/FFI.

## Rules

- `snake_case` modules/functions, `CamelCase` types, `SCREAMING_SNAKE_CASE` consts.
- No `.unwrap()`/`.expect()` in production paths without waiver; map errors with `Result`/`thiserror`/`anyhow`.
- Own data, avoid shared mutable state; lifetimes explicit; `Arc<Mutex<_>>` only at boundaries.
- Validate at the boundary with typed deserializers (serde); internal code uses deserialized types.
- Prefer `&str`/`&[T]` over owned data in APIs where possible; enums for closed sets.
- Async: never block in async tasks; structured concurrency; `Send + Sync` bounds documented at boundaries.
- Unsafe code: minimal, isolated, with `// SAFETY:` rationale; FFI inputs validated before crossing.
- Memory: avoid leaks in long-lived tasks; use `Drop` for cleanup; `Arc`/`Weak` to break cycles.

## Examples

- `examples/good-vs-bad/rust.md` (ownership, Result, async)
- `checks/coverage-thresholds.md`
- Waivers: `docs/waivers.md`
