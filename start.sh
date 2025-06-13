#!/usr/bin/env bash

# Run migrations
echo "Running migrations..."
python manage.py migrate --no-input

# Create superuser from environment variables
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='${DJANGO_SUPERUSER_USERNAME:-admin}').exists():
    User.objects.create_superuser(
        '${DJANGO_SUPERUSER_USERNAME:-admin}',
        '${DJANGO_SUPERUSER_EMAIL:-admin@example.com}',
        '${DJANGO_SUPERUSER_PASSWORD}'
    )
    print('Superuser created successfully')
else:
    print('Superuser already exists')
"

# Start gunicorn server
echo "Starting gunicorn server..."
gunicorn codebysiri.wsgi:application --log-file -
