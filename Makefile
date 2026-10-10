.PHONY: check check-py check-waivers test

check: check-py check-waivers
	@echo "all local gates passed"

check-py:
	uvx ruff check . --config enforce/python/pyproject.toml
	uvx ruff format --check . --config enforce/python/pyproject.toml
	uvx black --check scripts/ tests/ --config enforce/python/pyproject.toml
	python3 scripts/check_waivers.py

check-waivers:
	python3 scripts/check_waivers.py

test:
	python3 -m coverage run -m pytest tests/ -q
	python3 -m coverage report --fail-under=80
