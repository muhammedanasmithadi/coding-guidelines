# ADR index

Decision records. One record per decision: context, options, decision, consequences.
Records are immutable once accepted; a change lands as a new record that supersedes the
old one (`Supersedes:` field). The bar for writing one is two real alternatives and high
reversal cost — see `docs/21-adr.md`.

| ADR  | Title                                                      | Status             |
| ---- | ---------------------------------------------------------- | ------------------ |
| 0001 | Template                                                   | proposed           |
| 0002 | Standardize health endpoints on /livez + /readyz           | accepted           |
| 0003 | Language support — Python/TS/Go now, Rust/Java/C# deferred | superseded by 0005 |
| 0004 | TypeScript 7 migration path via oxlint type-aware          | accepted           |
| 0005 | Add Rust and C language support                            | accepted           |
| 0006 | Move runtimes to latest stable and LTS majors              | accepted           |
| 0007 | Runtime major upgrade policy                               | accepted           |
| 0008 | Rationale routing and ADR integrity                        | accepted           |
