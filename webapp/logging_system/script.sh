#!/bin/bash

python manage.py makemigrations
python manage.py migrate

celery -A logging_system worker
celery -A logging_system beat 

python manage.py runserver
