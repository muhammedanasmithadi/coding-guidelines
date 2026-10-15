# C — Do vs Avoid

## Bounds and ownership

Do:

```c
if (len >= buf_cap) return ERR_RANGE;
memcpy(dst, src, len);
```

Avoid: `strcpy`, unchecked `memcpy`, implicit cast truncation.

## Cleanup

Do:

```c
err = open_resource(...);
if (err) goto cleanup;
cleanup:
    close_resource(...);
    return err;
```

Avoid: early returns that leak handles.
