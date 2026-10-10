# Commits — Do vs Avoid

Do (one intent, explains why):
```
feat(checkout): add idempotency key

Retries double-charged on timeout. Key dedupes in outbox table.
```

Avoid:
```
fix stuff
WIP
fixup! broke test
```

Gate: `commitlint --from HEAD~1 --to HEAD` with `commitlint.config.mjs`. Squash keeps `type(scope): subject`.
