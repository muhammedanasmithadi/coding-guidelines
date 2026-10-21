# Comments and ADRs — Do vs Avoid

Do (the fact lives in one place, and the place is checked):

```python
def apply_eu_vat(order: Order, rate: EuVatRate) -> Total:
    return order.subtotal * rate.factor
```

The invariant is in the type, the intent in the name, so there is nothing left to comment.

```python
def test_livez_readyz_split_per_adr_0002() -> None:
    assert probe("/livez").status == 200
```

The rationale about a line lives in a name; the ADR covers the approach.

```
# ADR 0008: Rationale routing and ADR integrity
- Status: accepted
- Context: the comment rule was stated three ways and enforced unevenly
- Options: (A) ADRs as catch-all; (B) route each rationale to its own container; (C) keep comments
- Decision: (B) — one canonical clause, each container enforced separately
- Consequences: docstrings leave the tree; the ADR set gains a supersede chain
- Enforcement: `scripts/check_tree.py` (blocking); `scripts/check-comments.sh` (advisory)
```

Avoid (prose that duplicates the code, and records that drift):

```python
# increment the retry counter
counter += 1
```

```python
"""Fail CI when waivers are expired."""


def check_waivers() -> None: ...
```

```python
# TODO: refactor this later
# old_name = legacy_call()
```

```
# ADR 0002: health endpoints
- Status: accepted
- Context: docs used the deprecated `/healthz`
- Decision: use /livez
```

Avoid also: editing an accepted ADR instead of superseding it, a superseding record with no `Supersedes:` link, a record with no `Options` field, and a decision with no `Enforcement:` line.

Gate: `scripts/check_tree.py` — `check_comments` (directives only), `check_docstrings` (ast), `check_adr_records` (fields, numbering, supersede chain), `check_adr_links` (dangling and unreferenced records), `check_waiver_adr_links`. `scripts/check-comments.sh` reports Rust/Kotlin/C/Go comments as advisory.
