#!/bin/bash

python manage.py makemigrations
python manage.py migrate


terminal -e celery -A logging_system worker
terminal -e celery -A logging_system beat 

python manage.py runserver
