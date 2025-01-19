#!/bin/bash

yes | python manage.py makemigrations
yes | python manage.py migrate

python manage.py test

# celery -A logging_system worker -l Info
# celery -A logging_system beat -l info

python manage.py runserver 0.0.0.0:80
