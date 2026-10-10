# Error handling (bad vs good)

Bad — swallows, leaks internals:

```python
try:
    charge(user)
except Exception:
    pass
```

Good — typed, retryable only, maps to contract:

```python
try:
    charge(user)
except RetryableError as e:
    retry_with_backoff(e)
except DomainError as e:
    raise PublicError("charge failed") from e
```
