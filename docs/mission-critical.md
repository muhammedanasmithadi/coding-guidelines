# Mission-critical robustness tier

Standard tier is this repo's default gates. The mission-critical tier applies to
code where failure costs lives, hardware, or irreversible loss. It adapts NASA
JPL, MISRA, DO-178C, and hardware practice to Python/TypeScript services.
Sources: Holzmann Power of 10 https://en.wikipedia.org/wiki/The_Power_of_10:_Rules_for_Developing_Safety-Critical_Code (primary PDF unretrieved — rules via secondary), MISRA structure https://en.wikipedia.org/wiki/MISRA_C (rule texts proprietary — substance via Cppcheck checkers), DO-178C https://en.wikipedia.org/wiki/DO-178C (paid standard — high level only), WCET https://en.wikipedia.org/wiki/Worst-case_execution_time, watchdog https://en.wikipedia.org/wiki/Watchdog_timer, heartbeat https://en.wikipedia.org/wiki/Heartbeat_(computing)

## Adapted rules (all normative at this tier)

1. Simple control flow: no `eval`/metaprogramming tricks hiding control flow. Every loop has an explicit bound or timeout. (JPL 1, 2)
2. No unbounded growth in the hot path: preallocate pools, cap queue depths, shed load. No unbounded recursion — iterate or cap depth. (JPL 1, 3; MISRA 17.2, 21.3)
3. Small units with contracts: functions stay inside standard gates; preconditions validated at boundaries, postconditions asserted. Invariants use side-effect-free checks with explicit recovery — never bare `assert` in production paths. (JPL 4, 5)
4. Narrowest scope; check every return: no discarded `Result`/errors, validate all inputs. (JPL 6, 7; MISRA 17.7)
5. No hidden code: no dynamic dispatch tricks, no conditional-compilation equivalents without review. (JPL 8, 9)
6. Strictest toolchain from day one, zero warnings: `ruff --max-warnings=0` equivalent, `tsc --noEmit` strict, plus a strong analyzer in CI. (JPL 10)
7. Independence: author ≠ approver on critical paths. Requirements → code → test traceability via ticket IDs. Branch-condition tests (MC/DC-style), not just line coverage, for the critical tier. (DO-178C)
8. Timing budgets per handler with timeouts and load-shedding — the WCET analog. Liveness + readiness probes with supervisor restarts — the watchdog/heartbeat analog.
9. Deviation process, not silent exceptions: MISRA-style — Mandatory rules always hold; Required rules need a filed deviation (rule ID + safety rationale, our `waivers/` with expiry); Advisory needs only a record.

## Tiers

- Standard: default gates in `checks/`.
- Critical: above rules + independent review + traceability + MC/DC-style tests. Declare the tier per service in its README; mixed tiers live in separate modules with explicit boundaries.

## Examples

- `docs/incident.md` (response), `docs/runbook-template.md` (per-alert procedure), `docs/waivers.md` (deviation record)
