# Kotlin — Do vs Avoid

## Null safety

Do:

```kotlin
fun length(s: String?): Int = s?.length ?: 0
```

Avoid: `s!!` in production; handle null explicitly.

## Sealed/exhaustive

Do:

```kotlin
sealed interface Result
data class Ok(val value: Int) : Result
data class Err(val msg: String) : Result

fun handle(r: Result): String = when (r) {
    is Ok -> r.value.toString()
    is Err -> r.msg
}
```

Avoid: open hierarchies with `else` defaults.
