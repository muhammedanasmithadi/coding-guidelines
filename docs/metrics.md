# Metrics

Track monthly:

- Sonar new-code gate pass %, duplication %, maintainability rating.
- Patch coverage % (Codecov), line/branch coverage vs 80% floor.
- Waiver count + expired count + mean age. Alert on growth.
- DORA: lead time, deploy frequency, change failure rate, MTTR.
- False-positive rate per rule. Demote noisy rules to warning.

Export to `metrics/` or existing dashboard. Review in quarterly audit.
