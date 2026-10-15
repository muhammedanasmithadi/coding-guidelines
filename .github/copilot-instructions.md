# Repo-specific instructions for Copilot

This repository is a coding-guidelines project. Every change must keep `make check`,
`python -m pytest`, `npm run check`, `ruff`, `mypy`, `check_tree.py`, and `check_waivers.py`
green.

Rules:

- No comments in code except machine directives.
- Documentation changes need an `## Examples` section.
- Waivers need an owner, reason, and expiry within 90 days.
- Cite authoritative sources for any rule change.
- Do not edit auto-generated files without updating the generator.
- Keep Principles as normative text; tool configs are reference implementations.

When improving:

1. Run the full check suite.
2. Prefer small, sourced, test-backed changes.
3. Open a PR rather than pushing directly to `main`.
