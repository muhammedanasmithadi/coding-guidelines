.PHONY: check check-py check-waivers test spell

check: check-py check-waivers spell
	@echo "all local gates passed"

check-py:
	uvx ruff check . --config enforce/python/pyproject.toml
	uvx ruff format --check . --config enforce/python/pyproject.toml
	uvx black --check scripts/ tests/ --config enforce/python/pyproject.toml
	uvx --with types-pyyaml mypy scripts/ --config-file enforce/python/pyproject.toml
	python3 scripts/check_waivers.py
	python3 scripts/check_tree.py

check-waivers:
	python3 scripts/check_waivers.py

test:
	python3 -m coverage run -m pytest tests/ -q
	python3 -m coverage report --include="scripts/*,tests/*" --fail-under=80

spell:
	npx cspell --no-progress --fail-fast --config enforce/cspell.yaml "**/*.md"
