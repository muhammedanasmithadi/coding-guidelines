# Rust — Do vs Avoid

## Ownership and borrowing

Do:

```rust
fn word_count(text: &str) -> usize { text.split_whitespace().count() }
```

Avoid: unnecessary `.clone()` in hot loops; pass `&str`/`&[T]`.

## Result instead of panic

Do:

```rust
fn parse_port(s: &str) -> Result<u16, ParsePortError> { ... }
```

Avoid: `.unwrap()` in production paths.
