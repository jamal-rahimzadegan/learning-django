# ============================================================
# Configuration
# ============================================================

PORT ?= 8000
HOST ?= 127.0.0.1
REDIS_PORT ?= 6379

UV := uv run

# ============================================================
# Django & Setup
# ============================================================

.PHONY: install lock requirements start start-prod test dev migrate

# Syncs the environment with pyproject.toml / uv.lock
install:
	uv sync

# Updates the uv.lock file based on pyproject.toml
lock:
	uv lock

# Exports uv.lock to requirements.txt for deployments/Docker if needed
requirements:
	uv export --format requirements-txt --no-dev > requirements.txt

start:
	$(UV) python manage.py runserver $(HOST):$(PORT)

start-prod:
	$(UV) gunicorn myproject.wsgi:application --bind $(HOST):$(PORT) --workers 3

test:
	$(UV) pytest -v

dev: migrate start

migrate:
	$(UV) python manage.py makemigrations
	$(UV) python manage.py migrate

# ============================================================
# Celery
# ============================================================

.PHONY: celery-worker celery-beat

ifeq ($(OS),Windows_NT)
celery-worker:
	$(UV) celery -A backend worker -l info --pool=solo
else
celery-worker:
	$(UV) celery -A backend worker -l info
endif

celery-beat:
	$(UV) celery -A backend beat -l info

# ============================================================
# Redis
# ============================================================

.PHONY: redis-start redis-stop redis-check

redis-start:
	docker start social-event-redis

redis-stop:
	docker stop social-event-redis

redis-check:
	docker exec social-event-redis redis-cli ping

# ============================================================
# Docker
# ============================================================

.PHONY: docker-build docker-run

docker-build:
	docker build -t social-event-app .

docker-run:
	docker run -p $(PORT):8000 social-event-app