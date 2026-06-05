#!/bin/bash
# Exit immediately if a command exits with a non-zero status
set -e

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --no-input

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Start Gunicorn binding to the dynamic PORT environment variable (default to 8000)
PORT_NUM=${PORT:-8000}
echo "Starting Gunicorn on port $PORT_NUM..."
exec gunicorn real_estate.wsgi:application --bind 0.0.0.0:$PORT_NUM
