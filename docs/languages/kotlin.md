# Kotlin

Sources: Kotlin coding conventions https://kotlinlang.org/docs/coding-conventions.html, Android Kotlin style guide https://developer.android.com/kotlin/style-guide, ktlint https://github.com/pinterest/ktlint, detekt https://detekt.dev/

## Enforce

- Format: `ktlint --check` or `ktfmt --dry-run`; config via `.editorconfig` + `enforce/kotlin/detekt.yml`.
- Lint: `detekt --config enforce/kotlin/detekt.yml` (complexity, style, coroutines, null safety).
- Types/null: Kotlin nullable types are the type system; no `!!` in production paths without waiver; `kotlinx.validation` or kotlinx.serialization at boundaries.
- Test: JUnit 5 / Kotest; `./gradlew test`; jacocoTestReport with >=80% coverage (TEAM CHOICE).
- Concurrency: structured concurrency only; no `GlobalScope`; `Flow`/`Channel` with backpressure.
- Security: input validation at boundary; no reflection/deserialization of untrusted data.

## Rules

- `camelCase` vars/functions, `PascalCase` classes/types, enums UPPER or Pascal as domain requires.
- Prefer `val`, immutability, data classes for value objects; no mutable shared state.
- Validate at boundary with serialization/validation library.
- Sealed classes/interfaces for closed sets; exhaustive `when` with no `else` branch where possible.

## Examples

- `examples/good-vs-bad/kotlin.md` (null safety, sealed `when`, Flow)
- `docs/17-concurrency.md`
- Waivers: `docs/waivers.md`
