
# Makefile for orchestration-svc: world-class developer experience

.PHONY: help lint typecheck test coverage clean run format install pip-audit sbom pre-commit-install

help:
	@echo "Available targets:"
	@echo "  install    - Install dependencies with Poetry"
	@echo "  lint       - Run ruff and flake8 linting"
	@echo "  typecheck  - Run mypy type checking"
	@echo "  test       - Run all tests"
	@echo "  coverage   - Run tests with coverage report"
	@echo "  clean      - Remove all Python/mypy/pytest caches"
	@echo "  run        - Run the service locally (dev mode)"
	@echo "  format     - Run black code formatter"
	@echo "  pip-audit  - Run pip-audit for dependency vulnerability scanning"
	@echo "  sbom       - Generate CycloneDX SBOM (sbom.xml) for dependencies"
	@echo "  pre-commit-install - Install pre-commit hooks for this repo"

install:
	poetry install

lint:
	poetry run ruff check .
	poetry run flake8 src/orchestration_svc/ tests/

typecheck:
	poetry run mypy src/orchestration_svc/ tests/

test:
	poetry run pytest

coverage:
	poetry run pytest --cov=src/orchestration_svc --cov=tests --cov-report=term-missing

clean:
	rm -rf .mypy_cache .pytest_cache **/__pycache__

run:
	poetry run uvicorn src.orchestration_svc.main:app --reload

format:
	poetry run ruff format .
check:
	make lint
	make typecheck
	make test
	make pip-audit

ci:
	make check
	make sbom

pip-audit:
	poetry run pip-audit

sbom:
	pip install --user cyclonedx-bom > /dev/null 2>&1 || true
	sh scripts/generate_sbom.sh

pre-commit-install:
	poetry run pip install pre-commit > /dev/null 2>&1 || true
	poetry run pre-commit install
