.PHONY: check check-py check-ts check-waivers test spell links

check: check-py check-ts check-waivers spell links
	@echo "all local gates passed"

check-py:
	uvx ruff==0.17.0 check . --config enforce/python/pyproject.toml
	uvx ruff==0.17.0 format --check . --config enforce/python/pyproject.toml
	uvx --with types-pyyaml mypy==2.4.0 scripts/ --config-file enforce/python/pyproject.toml
	python3 scripts/check_waivers.py
	python3 scripts/check_tree.py

check-ts:
	npm run check

check-waivers:
	python3 scripts/check_waivers.py

test:
	python3 -m coverage run -m pytest tests/ -q
	python3 -m coverage report --include="scripts/*,tests/*" --fail-under=85

spell:
	npx cspell --no-progress --fail-fast --config enforce/cspell.yaml "**/*.md"

links:
	@if command -v lychee >/dev/null 2>&1; then lychee --no-progress './*.md' './docs/**/*.md' './checks/**/*.md' './examples/**/*.md' './.github/**/*.md'; else echo "lychee not installed; CI enforces links"; fi
release:
	npm run check
	npx oxfmt --check CHANGELOG.md package.json
	python3 scripts/check_tree.py
	npx cspell --no-progress --fail-fast --config enforce/cspell.yaml "**/*.md"
	@echo "release gates passed"
