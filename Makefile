.PHONY: help dev setup clean docker-build docker-up docker-down docker-logs docker-exec ollama-pull test lint format

# Default model to use
MODEL ?= tinyllama:latest

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Install dependencies
	pip install -r requirements.txt
	mkdir -p data/uploads

dev: ## Run the application locally with hot reload
	@echo "Starting development server..."
	PYTHONPATH=$(PWD) LOG_LEVEL=debug uvicorn src.main:app --reload --host 0.0.0.0 --port 8081 --log-config log_config.json

docker-build: ## Build Docker images
	@echo "Building Docker images..."
	docker-compose build

docker-up: ## Start all services in Docker
	@echo "Starting all services..."
	docker-compose up -d
	@echo "Services started! API available at http://localhost:8081"
	@echo "API documentation at http://localhost:8081/docs"

docker-down: ## Stop all Docker services
	@echo "Stopping all services..."
	docker-compose down

docker-down-volumes: ## Stop all Docker services and remove volumes
	@echo "Stopping all services and removing volumes..."
	docker-compose down -v

docker-logs: ## Show logs from all services
	docker-compose logs -f

docker-logs-app: ## Show logs from the app service only
	docker-compose logs -f app

docker-exec: ## Execute a command in the app container
	docker-compose exec app $(cmd)

ollama-pull: ## Pull a model in Ollama (default: tinyllama:latest)
	@echo "Pulling model $(MODEL)..."
	docker exec -it llm-project-ollama-1 ollama pull $(MODEL)

bootstrap: docker-build docker-up ollama-pull ## Build, start services and pull the default model

test: ## Run tests
	pytest tests/

lint: ## Run linting
	flake8 src/

format: ## Format code with black
	black src/

clean: ## Clean up temporary files and directories
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".benchmarks" -exec rm -rf {} +
	rm -rf .coverage coverage.xml htmlcov/ .pytest_cache/ 