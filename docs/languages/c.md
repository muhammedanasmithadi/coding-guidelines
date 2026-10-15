# C

Sources: CERT C Secure Coding https://wiki.sei.cmu.edu/confluence/display/c, C standard https://www.iso.org/standard/74534.html, clang-format https://clang.llvm.org/docs/ClangFormat.html, clang-tidy https://clang.llvm.org/extra/clang-tidy/

## Enforce

- Format: `clang-format --dry-run -Werror` using `enforce/c/.clang-format`.
- Lint/analysis: `clang-tidy` (`enforce/c/.clang-tidy`) plus `cppcheck --enable=all --error-exitcode=1`.
- Tests: CTest (or Criterion/CUnit); `ctest --output-on-failure`.
- Sanitizers in CI: `-fsanitize=address,undefined` for tests; thread sanitizer for threaded code.
- Coverage: `gcov`/`lcov` or `llvm-cov`, gate >=80% (TEAM CHOICE).
- Security: treat CERT C mandatory rules as blocking; MISRA rules require deviations (`docs/waivers.md`).

## Rules

- No undefined behavior: bounds-checked access, checked arithmetic, initialized variables, no dangling pointers.
- Memory ownership: every allocation has one owner and a documented free path; use arena/region allocators where possible.
- Errors via return codes or `errno`; no silent truncation; check every return.
- Validate at boundary (input length, ranges, encoding); use sized buffers, never unbounded reads.
- Prefer `const`-correct, minimal scope, RAII-style cleanup via goto cleanup labels or helper structs.
- No dynamic dispatch tricks or macro-heavy control flow without review.

## Examples

- `examples/good-vs-bad/c.md` (bounds, ownership, cleanup)
- `docs/mission-critical.md` (tier rules)
- Waivers: `docs/waivers.md`
