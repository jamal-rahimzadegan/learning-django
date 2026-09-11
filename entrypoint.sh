#!/bin/sh

# Wait until Postgres is ready to take queries
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL is up and running."

# Generate missing migration files
python manage.py makemigrations events

# Run migrations automatically for BOTH databases on startup
python manage.py migrate --database=default
python manage.py migrate --database=social_event

# Start Django app
exec "$@"