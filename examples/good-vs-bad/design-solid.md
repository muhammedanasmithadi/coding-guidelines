# Design / SOLID — Do vs Avoid

Sources: https://refactoring.guru/, https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design

## S — Single Responsibility

Do:
```python
class OrderPricer:
    def total(self, items):
        return sum(i.price for i in items)


class OrderRepo:
    def save(self, order): ...
```

Avoid: `OrderManager` prices + saves + emails + logs. Tax change retests email.

## O — Open/Closed

Do:
```python
class Discount:
    def apply(self, p): ...


class VipDiscount(Discount):
    def apply(self, p):
        return p * 0.8
```

Avoid:
```python
if customer.type == "vip":
    ...  # smell: edit tested code per type
elif customer.type == "staff":
    ...
```

## L — Liskov

Do: `Sparrow(Bird).fly()` preserves contract. Flightless birds sit outside `Bird`.

Avoid: `Penguin(Bird).fly() -> raise`. Callers branch on type. Classic `Square(Rectangle)` breaks `area = w*h`.

## I — Interface Segregation

Do:
```python
class Printer:
    def print(self, d): ...


class Scanner:
    def scan(self): ...
```

Avoid: `IMachine(print, scan, fax, staple)` forces `SimplePrinter.fax -> raise`.

## D — Dependency Inversion

Do:
```python
class Notifier(Protocol):
    def send(self, m): ...


class Checkout:
    def __init__(self, n: Notifier):
        self.n = n
```

Avoid:
```python
from smtp import SmtpClient  # smell: concrete in policy, untestable

SmtpClient().send()
```

## Composition

Do: `ApiHandler(auth: Authorizer)` composes. Avoid: 5-level `AdminHandler(Handler)` fragile base.

## Boundaries — no cycles

Do: `api -> service -> repo`. `billing` imports `orders.api`, never reverse.

Avoid: `orders imports billing; billing imports orders`. Circular import, untestable.
