# ============================================================
# Configuration
# ============================================================

PORT ?= 8000
HOST ?= 127.0.0.1
REDIS_PORT ?= 6379

# Detect Windows
ifeq ($(OS),Windows_NT)
    PYTHON := ./venv/bin/python #python
    PIP := python -m pip
else
    PYTHON := ./venv/bin/python #python3
    PIP := python3 -m pip
endif

# ============================================================
# Django
# ============================================================

.PHONY: start start-prod requirements install dev migrate

start:
	#./venv/bin/python manage.py runserver 127.0.0.1:8000
	$(PYTHON) manage.py runserver $(HOST):$(PORT)

test:
	pytest -v

start-prod:
	gunicorn myproject.wsgi:application --bind $(HOST):$(PORT) --workers 3

requirements:
	$(PIP) freeze > requirements.txt

install:
	$(PIP) install -r requirements.txt

dev: migrate start

migrate:
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate

# ============================================================
# Celery
# ============================================================

.PHONY: celery-worker celery-beat

ifeq ($(OS),Windows_NT)
celery-worker:
	celery -A backend worker -l info --pool=solo
else
celery-worker:
	celery -A backend worker -l info
endif

celery-beat:
	celery -A backend beat -l info

# ============================================================
# Redis
# ============================================================

.PHONY: redis-check redis-start redis-stop

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