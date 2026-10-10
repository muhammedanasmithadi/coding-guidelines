# 05 Commits

- Format: Conventional Commits https://www.conventionalcommits.org/en/v1.0.0/. Lint: `commitlint --from --to`.
- Version: SemVer https://semver.org/. Changelog: Keep a Changelog https://keepachangelog.com/en/1.0.0/.
- Scope small. One intent per commit. Message explains why, diff shows what.
- No `fixup!`/`WIP` on main. Squash merges keep `type(scope): subject`.

Check: commitlint + lychee for changelog links + cspell for typos.
