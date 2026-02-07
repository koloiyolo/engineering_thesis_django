#!/bin/bash

yes | uv run python3 manage.py makemigrations
yes | uv run python3 manage.py migrate

uv run python3 manage.py test

# celery -A logging_system worker -l Info
# celery -A logging_system beat -l info

uv run python3 manage.py runserver 0.0.0.0:80
