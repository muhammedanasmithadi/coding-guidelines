# Python — Do vs Avoid

Sources: PEP 8 https://peps.python.org/pep-0008/, Google Python https://google.github.io/styleguide/pyguide.html, pydantic https://docs.pydantic.dev/latest/, Hypothesis https://hypothesis.readthedocs.io/en/latest/

## 1. Naming

Do:

```python
MAX_RETRIES = 3


class HttpClient: ...


def fetch_user(user_id: int) -> User: ...
```

Avoid — mixedCase, cryptic:

```python
def FetchUser(l, O): ...  # smell: unreadable, confuses l/1 O/0
```

## 2. Functions — small, pure

Do:

```python
def total(items: list[Line]) -> Decimal:
    return sum((i.price * i.qty for i in items), Decimal(0))
```

Avoid — god function with globals + I/O:

```python
def do_stuff():  # smell: 150 lines, mutates CACHE, mixes I/O + calc
    global CACHE
    ...open(...); ...requests...; CACHE[...] = ...
```

## 3. Classes — cohesive, DI

Do:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Employee:
    name: str
    salary: int


class PayService:
    def __init__(self, repo: Repo):
        self._repo = repo
```

Avoid — shared mutable class var:

```python
class Dog:
    tricks = []  # smell: shared by all instances
```

## 4. Errors — typed, narrow

Do:

```python
try:
    value = collection[key]
except KeyError:
    return key_not_found(key)
else:
    return handle_value(value)
```

Avoid — blind catch:

```python
try:
    return handle_value(collection[key])
except:  # smell: catches KeyboardInterrupt/SystemExit, hides bugs
    return None
```

## 5. Logging — logger + structlog

Do:

```python
import logging

log = logging.getLogger(__name__)
log.info("order_created", extra={"order_id": oid})
```

Avoid:

```python
print(f"order created {oid}")  # smell: no level, timestamp, JSON
```

## 6. Config — pydantic-settings

Do:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_")
    port: int = 5432
    api_key: str
```

Avoid:

```python
API_KEY = "sk-live-123"  # smell: secret in code, per-env forks
```

## 7. Validation — pydantic model

Do:

```python
from pydantic import BaseModel, PositiveInt


class User(BaseModel):
    id: int
    tastes: dict[str, PositiveInt]
```

Avoid — ad-hoc chains:

```python
if not isinstance(data["id"], int):
    raise ValueError(...)  # smell: incomplete, no schema export
```

## 8. Async — deadline

Do:

```python
async with asyncio.timeout(10):
    await long_running_task()
```

Avoid:

```python
await eternity()  # smell: hangs forever, no cancel
```

## 9. Testing — fixtures + property

Do:

```python
@pytest.fixture
def client(db):
    c = make_client(db)
    yield c
    c.close()


@given(st.lists(st.integers()))
def test_sort(lst):
    assert sorted(my_sort(lst)) == my_sort(lst)
```

Avoid:

```python
assert my_sort([3, 1, 2]) == [1, 2, 3]  # smell: 1 example, misses edges
```

## 10. Typing — strict

Do:

```python
def greeting(name: str) -> str:
    return "Hello " + name


# gate: mypy --strict
```

Avoid:

```python
def greeting(name):  # type: ignore  # smell: Any everywhere
    return "Hello " + name
```
