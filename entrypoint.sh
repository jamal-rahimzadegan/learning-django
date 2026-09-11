#!/bin/sh

echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL is up and running."

# Generate missing migration files
python manage.py makemigrations events

# Run migrations for BOTH databases
python manage.py migrate --database=default
python manage.py migrate --database=social_event

# Automate superuser creation on the default database
# Do not create user here it's not a good practice to create superuser in entrypoint.sh, but for the sake of this example, we will do it.
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('Superuser admin created successfully.')
else:
    print('Superuser admin already exists.')
"

exec "$@"