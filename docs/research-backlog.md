# Research backlog for guideline improvements

Sources: public and permissive materials only. Cite the source in the rule doc. Do not copy verbatim text from copyrighted books.

## Candidate topics

- Error handling and resilience patterns (retry, circuit breaker, bulkhead).
- API design: pagination, idempotency, versioning, deprecation.
- Concurrency: data races, deadlocks, cancellation, timeouts.
- Security: OWASP Top 10, supply chain, secrets management.
- Observability: RED/USE metrics, tracing, SLOs.
- Testing: property-based testing, mutation testing, contract testing.
- Performance: budgets, profiling, caching strategies.
- Accessibility and i18n.

## Process

1. Pick one topic.
2. Research public sources (official docs, open-source style guides, OWASP, RFCs).
3. Draft an ADR + doc update + enforcement check.
4. Open a PR with tests and examples.
5. Review and merge.

## Examples

- docs/adr/0001-template.md
- docs/04-security.md