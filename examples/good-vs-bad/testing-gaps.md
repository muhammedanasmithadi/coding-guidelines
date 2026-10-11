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
Avoid: match `/id="source"/` — one Prettier run turns the suite red (observed live).
