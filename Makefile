"""Makefile-style commands for project management."""

.PHONY: help install dev test lint format clean docker-build docker-up docker-down migrate revision

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	pip install -r requirements.txt

dev:  ## Run development server
	chmod +x start-dev.sh
	./start-dev.sh

test:  ## Run tests
	pytest -v --cov=app --cov-report=html --cov-report=term-missing

test-unit:  ## Run unit tests only
	pytest -v -m unit

test-integration:  ## Run integration tests only
	pytest -v -m integration

lint:  ## Run linters
	ruff check .
	mypy app

format:  ## Format code
	ruff format .

clean:  ## Clean up generated files
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage

docker-build:  ## Build Docker image
	docker-compose build

docker-up:  ## Start Docker containers
	docker-compose up -d

docker-down:  ## Stop Docker containers
	docker-compose down

docker-logs:  ## Show Docker logs
	docker-compose logs -f

migrate:  ## Run database migrations
	alembic upgrade head

revision:  ## Create new migration revision
	@read -p "Enter migration message: " message; \
	alembic revision --autogenerate -m "$$message"

downgrade:  ## Rollback one migration
	alembic downgrade -1

db-reset:  ## Reset database (drop all and recreate)
	alembic downgrade base
	alembic upgrade head

shell:  ## Open Python shell with app context
	python -c "from app.core.config import settings; print(settings)"

requirements:  ## Update requirements.txt from current environment
	pip freeze > requirements.txt
