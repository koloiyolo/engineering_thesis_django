#!/bin/bash
sleep 45

python manage.py makemigrations
python manage.py migrate

# celery -A logging_system worker -l Info
# celery -A logging_system beat -l info

python manage.py runserver 0.0.0.0:8000
