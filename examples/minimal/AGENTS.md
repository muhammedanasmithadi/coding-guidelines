# Agent instructions

Follow the coding guidelines pinned by this repo.

Before coding:
- Read `docs/01-principles.md`, `docs/languages/<lang>.md`, and `CONTEXT.md` if present.
- Run the stack's documented checks before claiming done.

Rules:
- No comments in code except machine directives.
- Keep functions <50 lines, CC<15, files <200 LOC.
- Validate at boundaries; return typed errors.
- Tests for every behavior change; no network/disk/clock in tests without fakes.

Verification:
- Run `make check` or the documented stack commands.
- Do not merge until CI is green.