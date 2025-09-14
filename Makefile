# MOSAIC Plane Info - Development Makefile
.PHONY: help install dev build test clean docker-build docker-up docker-down docker-logs cf-deploy-dev cf-deploy-prod cf-dev cf-tail

# Configuration variables
PLAYWRIGHT_VERSION := v1.55.0
PLAYWRIGHT_IMAGE := mcr.microsoft.com/playwright:$(PLAYWRIGHT_VERSION)-jammy

# Default target
help:
	@echo "Available targets:"
	@echo "  install      - Install dependencies for both API and UI"
	@echo "  dev          - Start development servers (API and UI)"
	@echo "  build        - Build production assets"
	@echo "  test         - Run all tests"
	@echo "  e2e          - Run E2E tests with Playwright using Docker Compose stack"
	@echo "  e2e-headed   - Run E2E tests with headed browser using Docker Compose stack"
	@echo "  clean        - Clean build artifacts and dependencies"
	@echo "  precommit    - Run pre-commit hooks in Docker container"
	@echo ""
	@echo "Docker targets:"
	@echo "  docker-build - Build Docker containers"
	@echo "  docker-up    - Start services with Docker Compose"
	@echo "  docker-down  - Stop Docker Compose services"
	@echo "  docker-logs  - Show Docker Compose logs"
	@echo ""
	@echo "Cloudflare deployment:"
	@echo "  cf-deploy-dev     - Deploy UI to Cloudflare Workers (development)"
	@echo "  cf-deploy-prod    - Deploy UI to Cloudflare Workers (production)"
	@echo "  cf-dev            - Start local Cloudflare Workers development"
	@echo "  cf-tail           - View Cloudflare Workers logs"
	@echo ""
	@echo "Individual targets:"
	@echo "  api-install  - Install Python dependencies"
	@echo "  api-dev      - Start Django development server"
	@echo "  api-test     - Run Django tests"
	@echo "  api-typecheck - Run mypy type checking on Django API"
	@echo "  ui-install   - Install Node.js dependencies"
	@echo "  ui-dev       - Start Vue development server"
	@echo "  ui-test      - Run Vue tests"
	@echo "  ui-build     - Build production Vue assets"

# Install all dependencies
install: api-install ui-install

# Start both development servers
dev:
	@echo "Starting development servers..."
	@echo "API will be available at http://localhost:8000"
	@echo "UI will be available at http://localhost:3000"
	@$(MAKE) -j2 api-dev ui-dev

# Build production assets
build: ui-build

# Run all tests
test: api-test ui-test

# E2E tests with Playwright in Docker
e2e:
	@echo "Starting Docker Compose services for E2E testing..."
	docker compose up -d
	@echo "Waiting for services to be healthy..."
	@timeout=120; \
	while [ $$timeout -gt 0 ]; do \
		if curl -f http://localhost:8080 >/dev/null 2>&1; then \
			echo "✅ Application is responding on port 8080"; \
			break; \
		fi; \
		echo "⏳ Waiting for application to start..."; \
		sleep 5; \
		timeout=$$((timeout - 5)); \
	done; \
	if [ $$timeout -le 0 ]; then \
		echo "❌ Application failed to start on port 8080"; \
		docker compose logs; \
		docker compose down; \
		exit 1; \
	fi
	@echo "Running E2E tests with Playwright in Docker container..."
	docker run --rm --network host \
		-e DOCKER_E2E=true \
		-v $(PWD)/src/ui:/work \
		-w /work \
		$(PLAYWRIGHT_IMAGE) \
		bash -c "npm ci && npx playwright test"
	@echo "Stopping Docker Compose services..."
	docker compose down

# E2E tests with headed browser (for debugging)
e2e-headed:
	@echo "Starting Docker Compose services for E2E testing..."
	docker compose up -d
	@echo "Waiting for services to be healthy..."
	@timeout=120; \
	while [ $$timeout -gt 0 ]; do \
		if curl -f http://localhost:8080 >/dev/null 2>&1; then \
			echo "✅ Application is responding on port 8080"; \
			break; \
		fi; \
		echo "⏳ Waiting for application to start..."; \
		sleep 5; \
		timeout=$$((timeout - 5)); \
	done; \
	if [ $$timeout -le 0 ]; then \
		echo "❌ Application failed to start on port 8080"; \
		docker compose logs; \
		docker compose down; \
		exit 1; \
	fi
	@echo "Running E2E tests with headed browser in Docker container..."
	docker run --rm --network host \
		-e DOCKER_E2E=true \
		-e DISPLAY=${DISPLAY} \
		-v /tmp/.X11-unix:/tmp/.X11-unix:rw \
		-v $(PWD)/src/ui:/work \
		-w /work \
		$(PLAYWRIGHT_IMAGE) \
		bash -c "npm ci && npx playwright test --headed"
	@echo "Stopping Docker Compose services..."
	docker compose down

# Pre-commit hooks execution
precommit:
	@echo "Running pre-commit hooks in Docker container..."
	docker run --rm \
		-v $(PWD):/work \
		-w /work \
		--env PRE_COMMIT_HOME=/tmp/.pre-commit \
		precommitci/pre-commit-with-plugins:latest \
		pre-commit run --all-files

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	cd src/api && find . -name "*.pyc" -delete
	cd src/api && find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	cd src/ui && rm -rf dist/ node_modules/.cache/
	docker system prune -f

# API targets
api-install:
	@echo "Installing Python dependencies..."
	cd src/api && python -m pip install --upgrade pip
	cd src/api && pip install -r requirements.txt

api-dev:
	@echo "Starting Django development server..."
	cd src/api && python manage.py migrate
	cd src/api && python manage.py seed_exact
	cd src/api && python manage.py runserver

api-test:
	@echo "Running Django tests..."
	cd src/api && python manage.py test

api-typecheck:
	@echo "Running mypy type checking on Django API..."
	cd src/api && python -m mypy .

# UI targets (using Docker containers for consistency)
ui-install:
	@echo "Installing Node.js dependencies using Docker container..."
	docker-compose run --rm ui npm install

ui-dev:
	@echo "Starting Vue development server using Docker container..."
	@echo "UI will be available at http://localhost:3000"
	docker-compose up ui

ui-test:
	@echo "Running Vue tests using Docker container..."
	docker-compose run --rm ui npm run test

ui-build:
	@echo "Building production Vue assets using Docker container..."
	docker-compose run --rm ui npm run build

# Docker targets
docker-build:
	@echo "Building Docker containers..."
	docker-compose build

docker-up:
	@echo "Starting services with Docker Compose..."
	@echo "Application will be available at http://localhost:8080 (nginx reverse proxy)"
	@echo "  - UI: http://localhost:8080/"
	@echo "  - API: http://localhost:8080/api/v1/"
	@echo "  - API Docs: http://localhost:8080/api/docs/"
	docker-compose up -d

docker-down:
	@echo "Stopping Docker Compose services..."
	docker-compose down

docker-logs:
	@echo "Showing Docker Compose logs..."
	docker-compose logs -f

# Cloudflare Workers deployment targets (using Docker containers)
cf-deploy-dev:
	@echo "Deploying UI to Cloudflare Workers (development) using Docker container..."
	docker-compose run --rm ui npm run deploy:dev

cf-deploy-prod:
	@echo "Deploying UI to Cloudflare Workers (production) using Docker container..."
	docker-compose run --rm ui npm run deploy:prod

cf-dev:
	@echo "Starting local Cloudflare Workers development server using Docker container..."
	docker-compose run --rm --service-ports ui npm run cf:dev

cf-tail:
	@echo "Showing Cloudflare Workers logs using Docker container..."
	docker-compose run --rm ui npm run cf:tail

