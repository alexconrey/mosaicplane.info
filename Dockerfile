# Multi-stage build for production deployment
# Stage 1: Build Vue.js frontend
FROM node:22-alpine AS ui-builder

WORKDIR /app/ui

# Copy package files
COPY src/ui/package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY src/ui/src ./src
COPY src/ui/index.html ./
COPY src/ui/vite.config.production.js ./vite.config.js

# Build production assets
RUN npm run build

# Stage 2: Production server
FROM python:3.11-slim AS production

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy and install Python dependencies
COPY src/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django application
COPY src/api/ ./api/

# Copy built UI assets from previous stage
COPY --from=ui-builder /app/ui/dist ./static/

# Create directories and app user
RUN mkdir -p /app/data && \
    addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --gid 1001 --home /app appuser && \
    chown -R appuser:appgroup /app

# Environment variables (can be overridden at runtime)
ENV DATABASE_URL=sqlite:///app/data/db.sqlite3
ENV API_BASE_URL=http://localhost:8000
ENV ENVIRONMENT=production
ENV DEBUG=False
ENV ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
ENV PORT=8000
ENV DJANGO_SETTINGS_MODULE=mosaicplane.settings

# Expose port (for local testing - ignored by Heroku)
EXPOSE 8000

# Create startup script that uses $PORT environment variable
RUN echo '#!/bin/bash\n\
set -e\n\
echo "=== MOSAIC Plane Info - Production Container ==="\n\
echo "Environment: $ENVIRONMENT"\n\
echo "API Base URL: $API_BASE_URL"\n\
echo "Database URL: $DATABASE_URL"\n\
echo "Port: $PORT"\n\
echo ""\n\
echo "Running database migrations..."\n\
cd /app/api && python manage.py migrate\n\
echo "Seeding database with aircraft data..."\n\
cd /app/api && python manage.py seed_exact\n\
echo "Collecting static files..."\n\
cd /app/api && python manage.py collectstatic --noinput\n\
echo "Starting Django server..."\n\
cd /app/api && python manage.py runserver 0.0.0.0:$PORT' > /app/start.sh

RUN chmod +x /app/start.sh && \
    chown appuser:appgroup /app/start.sh

# Switch to non-root user
USER appuser

# Run the application
CMD ["/app/start.sh"]