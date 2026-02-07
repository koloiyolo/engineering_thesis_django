FROM fedora:43

RUN dnf install uv mysql-devel cc celery -y

RUN uv python install 3.12

WORKDIR /app

COPY manage.py .
COPY script.sh .
COPY pyproject.toml .
COPY uv.lock .
COPY .python-version .
RUN uv sync
COPY script.sh .

COPY logging_system/ logging_system/

RUN chmod 777 script.sh

EXPOSE 80
