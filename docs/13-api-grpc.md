# 13 gRPC

- Fields 1-15 for hot paths (one wire byte). Never change or reuse a number. Source: https://protobuf.dev/programming-guides/proto3/#updating
- Additive-only evolution. `reserve` deleted numbers/names. Map errors to codes. Sources: https://protobuf.dev/programming-guides/proto3/#updating, https://grpc.io/docs/
- Check: `buf breaking` (or equivalent) in CI against `main`. Waivers: `docs/waivers.md`.

## Examples

- `examples/good-vs-bad/api.md` (numbering, compat)

Sources: https://protobuf.dev/programming-guides/proto3/#updating, https://grpc.io/docs/
