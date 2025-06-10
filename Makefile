.PHONY: help test docs clean install dev

help:
	@echo "Available commands:"
	@echo "  install     Install package in development mode"
	@echo "  dev         Install with development dependencies"
	@echo "  test        Run tests with coverage"
	@echo "  docs        Build documentation"
	@echo "  docs-serve  Build and serve documentation locally"
	@echo "  clean       Clean build artifacts"

install:
	pip install -e .

dev:
	pip install -e ".[dev,docs]"

test:
	pytest --cov=wave_view --cov-report=html --cov-report=term

docs:
	cd docs && make html

docs-serve: docs
	@echo "Documentation built. Opening in browser..."
	@cd docs && python -m http.server 8000 --directory _build/html

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf docs/_build/
	rm -rf docs/_autosummary/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete 