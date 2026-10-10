# Structure — Do vs Avoid

## Public surface

Do (`billing/__init__.py` re-exports only public names):
```python
from billing.pricing import Pricer

__all__ = ["Pricer"]
```

Avoid (deep import ossifies internals):
```python
from billing.pricing.v2.impl import _Pricer  # smell: breaks on refactor
```

## Layers

Do: `api -> service -> repo`. `billing` imports `orders.api`, never reverse.

Avoid: `orders imports billing; billing imports orders`. Circular, untestable.

Check: `ruff --select I`, `eslint import/no-cycle`.
