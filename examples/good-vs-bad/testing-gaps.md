# Testing gaps — Do vs Avoid

## Quarantine flaky

Do:

```python
import pytest


@pytest.mark.quarantine
def test_flaky_network(): ...


# default suite: pytest -m "not quarantine" -q
# quarantine job tracks with expiry ticket
```

Avoid: leaving flaky in default suite. Main red 30%, everyone re-runs, coverage gate meaningless.

## Fake clock / seeded RNG

Do:

```python
def test_expiry():
    clock = FakeClock(t0)
    assert Checkout(clock=clock).is_expired() is False
```

Avoid: `time.now()` / `Date.now()` / live `fetch(prod)` in unit. Flaky across TZ and retries.

## Mutation

Do: `stryker run` / `cargo mutants` on `pricing/`. Kill surviving mutants with new asserts.

Avoid: 100% line coverage that asserts nothing (`assert run()` with no check).

## Assert properties, not formatting

Do: match `/id=["']source["']/` — quote style is the formatter's business.
Avoid: match `/id="source"/` — one formatter run turns the suite red (observed live).

## Stupid unit tests agents write

Avoid:

```python
def test_parse():
    mock.return_value = {...}
    parse(input)
    assert mock.called
```

This checks the mock, not behavior.

Do:

```python
def test_rejects_malformed_header():
    result = parse("bad")
    assert result.status == "rejected"
    assert result.errors == ["bad header"]
```

Avoid:

```python
def test_quarantined():
    pytest.skip("flaky network")
```

Do: fix the fake boundary or quarantine with owner and expiry.

Avoid: 10 copies of `test_happy_path_1`...`test_happy_path_10` that differ only example text.

Do: table-driven cases with shared assertions, plus one mutation-aware assertion per boundary.
