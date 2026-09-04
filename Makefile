PYTHON ?= python

.PHONY: install lint test report verify

install:
	$(PYTHON) -m pip install -e '.[dev]'

lint:
	ruff check .
	ruff format --check .

test:
	pytest --cov=sql_ops_metrics --cov-report=term-missing --cov-fail-under=85 -q

report:
	sql-ops report --report evidence/sql-ops-report.json

verify: lint test report
