# Variables
PORT ?= 8000
HOST ?= 127.0.0.1
REDIS_PORT ?= 6379

# Declare all phony targets (non-file task shortcuts)
.PHONY: start start-prod requirements install dev migrate worker beat redis-start redis-stop redis-check install docker-build docker-run

start:
	python manage.py runserver $(HOST):$(PORT)
start-prod:
	gunicorn myproject.wsgi:application --bind $(HOST):$(PORT) --workers 3
requirements:
	pip freeze > requirements.txt
install:
	pip install -r requirements.txt
dev: migrate start

# Migration Management
migrate:
	python manage.py makemigrations
	python manage.py migrate


# Celery Management
celery-worker:
	celery -A backend worker -l info
celery-beat:
	celery -A backend beat -l info

# REDIS Management
redis-start:
	brew services start redis
redis-stop:
	brew services stop redis
redis-check:
	redis-cli ping


# Docker Management
docker-build:
	docker build -t social-event-app .
docker-run:
	docker run -p 8000:8000 social-event-app