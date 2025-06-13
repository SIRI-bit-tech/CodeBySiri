#!/usr/bin/env bash

# Run migrations
echo "Running migrations..."
python manage.py migrate --no-input

# Create SEO settings if they don't exist
echo "Creating SEO settings..."
python manage.py create_seo_settings

# Create superuser from environment variables
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth.models import User
try:
    if not User.objects.filter(username='${DJANGO_SUPERUSER_USERNAME:-admin}').exists():
        User.objects.create_superuser(
            '${DJANGO_SUPERUSER_USERNAME:-admin}',
            '${DJANGO_SUPERUSER_EMAIL:-admin@example.com}',
            '${DJANGO_SUPERUSER_PASSWORD}'
        )
        print('Superuser created successfully')
    else:
        print('Superuser already exists')
except Exception as e:
    print(f'Error creating superuser: {e}')
"

# Compress CSS/JS files for production
echo "Compressing static files..."
python manage.py compress --force

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

# Start gunicorn server
echo "Starting gunicorn server..."
gunicorn codebysiri.wsgi:application --log-file - --bind 0.0.0.0:$PORT
