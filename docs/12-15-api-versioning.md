# 12 REST, 13 gRPC, 14 GraphQL, 15 Versioning

## REST
- Nouns for resources. Status codes exact. Paginate with cursor. Sunset header for deprecations.
- Lint: `spectral lint openapi.yaml`, break check: `oasdiff breaking base.yaml head.yaml --fail-on ERR`.
- Source: https://github.com/microsoft/api-guidelines

## gRPC
- Stable field numbers. Never reuse. Map errors to codes. Source: https://grpc.io/docs/

## GraphQL
- Paginate connections. Deprecate fields, never remove without window. Source: https://graphql.org/learn/best-practices/

## Versioning
- SemVer https://semver.org/. API path `/v1`. Changelog per release.

## Examples
- `examples/good-vs-bad/api.md` (REST, gRPC, GraphQL, SemVer, migrations)
