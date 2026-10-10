# Good vs bad

## Function size (bad)

```python
def handle(req):  # 120 lines, CC 22
    ...
```

## Function size (good)

```python
def handle(req) -> Response:
    data = parse(req)  # raises ValidationError
    result = apply(data)
    return to_response(result)
```

Each helper stays <50 lines, CC<15. Test covers 80%+ branches.
