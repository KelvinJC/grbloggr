#!/bin/sh

until cd /app/src
do
    echo "Waiting for server volume..."
done


until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done


python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate


gunicorn grbloggr.wsgi --bind 0.0.0.0:8000  --workers 4 --threads 4

