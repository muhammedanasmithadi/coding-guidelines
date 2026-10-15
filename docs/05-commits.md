# 05 Commits

- Format: Conventional Commits https://www.conventionalcommits.org/en/v1.0.0/. Lint: `commitlint --from HEAD~1 --to HEAD` via `quality.yml` "Commit messages" step (config `commitlint.config.mjs`, deps `@commitlint/cli` + `@commitlint/config-conventional`).
- Version: SemVer https://semver.org/. Changelog: Keep a Changelog https://keepachangelog.com/en/1.0.0/.
- Scope small. One intent per commit. Message explains why, diff shows what.
- No `fixup!`/`WIP` on main. Squash merges keep `type(scope): subject`.

Check: commitlint + lychee for changelog links + cspell for typos.

Sources: https://www.conventionalcommits.org/en/v1.0.0/., https://semver.org/., https://keepachangelog.com/en/1.0.0/.

## Examples

- `examples/good-vs-bad/ai-slop.md` (agent failure modes + catches)

- `examples/good-vs-bad/commits.md`
