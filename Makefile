# Variables
PORT ?= 8000
HOST ?= 127.0.0.1
REDIS_PORT ?= 6379

# Declare all phony targets (non-file task shortcuts)
.PHONY: start start-prod dev migrate worker beat redis-start redis-stop redis-check

# Local Development Server (npm start equivalent)
start:
	python manage.py runserver $(HOST):$(PORT)

# Production Server (Business Standard)
start-prod:
	gunicorn myproject.wsgi:application --bind $(HOST):$(PORT) --workers 3

# Shortcut to apply migrations before starting
dev: migrate start

migrate:
	python manage.py makemigrations
	python manage.py migrate

# Celery Management

# Start a worker to execute tasks
celery-worker:
	celery -A backend worker -l info

# Start the Beat scheduler for timed/periodic tasks
celery-beat:
	celery -A backend beat -l info

# REDIS Management

# Start Redis background service
redis-start:
	brew services start redis

# Stop Redis background service
redis-stop:
	brew services stop redis

# Ping Redis to test connection (returns PONG if working)
redis-check:
	redis-cli ping