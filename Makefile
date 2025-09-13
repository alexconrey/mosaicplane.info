# MOSAIC Plane Info - Development Makefile
.PHONY: help install dev build test clean docker-build docker-up docker-down docker-logs docker-prod cf-deploy-dev cf-deploy-prod cf-dev cf-tail

# Default target
help:
	@echo "Available targets:"
	@echo "  install      - Install dependencies for both API and UI"
	@echo "  dev          - Start development servers (API and UI)"
	@echo "  build        - Build production assets"
	@echo "  test         - Run all tests"
	@echo "  clean        - Clean build artifacts and dependencies"
	@echo ""
	@echo "Docker targets:"
	@echo "  docker-build - Build Docker containers"
	@echo "  docker-up    - Start services with Docker Compose"
	@echo "  docker-down  - Stop Docker Compose services"
	@echo "  docker-logs  - Show Docker Compose logs"
	@echo "  docker-prod  - Build production Docker container with environment variables"
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

# UI targets
ui-install:
	@echo "Installing Node.js dependencies..."
	cd src/ui && npm install

ui-dev:
	@echo "Starting Vue development server..."
	cd src/ui && npm run dev

ui-test:
	@echo "Running Vue tests..."
	cd src/ui && npm run test

ui-build:
	@echo "Building production Vue assets..."
	cd src/ui && npm run build

# Docker targets
docker-build:
	@echo "Building Docker containers..."
	docker-compose build

docker-up:
	@echo "Starting services with Docker Compose..."
	@echo "API will be available at http://localhost:8000"
	@echo "UI will be available at http://localhost:3000"
	docker-compose up -d

docker-down:
	@echo "Stopping Docker Compose services..."
	docker-compose down

docker-logs:
	@echo "Showing Docker Compose logs..."
	docker-compose logs -f

# Cloudflare Workers deployment targets
cf-deploy-dev:
	@echo "Deploying UI to Cloudflare Workers (development)..."
	cd src/ui && npm run deploy:dev


cf-deploy-prod:
	@echo "Deploying UI to Cloudflare Workers (production)..."
	cd src/ui && npm run deploy:prod

cf-dev:
	@echo "Starting local Cloudflare Workers development server..."
	cd src/ui && npm run cf:dev

cf-tail:
	@echo "Showing Cloudflare Workers logs..."
	cd src/ui && npm run cf:tail

# Production Docker container target
docker-prod:
	@echo "Building production Docker container..."
	@echo "This will create a standalone container with:"
	@echo "  - Django server serving API and static assets"
	@echo "  - Built Vue.js static assets integrated into Django"
	@echo "  - Runtime environment variable configuration"
	docker build -t mosaicplane-info:production .
	@echo ""
	@echo "Production container built successfully!"
	@echo "Run with:"
	@echo "  docker run -p 8000:8000 mosaicplane-info:production"
	@echo ""
	@echo "Optional environment variables:"
	@echo "  -e API_BASE_URL=https://api.mosaicplane.info"
	@echo "  -e DATABASE_URL=sqlite:///app/data/db.sqlite3"
	@echo "  -e ENVIRONMENT=production"