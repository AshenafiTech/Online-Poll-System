#!/bin/bash
set -e

echo "Waiting for database..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo "Database is ready!"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput


# Optionally create superuser if CREATE_SUPERUSER is set
if [ "$CREATE_SUPERUSER" = "1" ]; then
  echo "Creating superuser..."
  python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists() or User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')"
fi

echo "Starting server..."
exec "$@"