#!/bin/bash
set -e

echo "Running database migrations..."
python manage.py migrate

echo "Initializing feature flags with default values..."
python manage.py initialize_feature_flags --reset

echo "Starting application..."
exec gunicorn mosaicplane.wsgi:application --bind 0.0.0.0:${PORT:-8000}