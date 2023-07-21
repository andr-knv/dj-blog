FROM python:3.11-alpine3.18

COPY requirements.txt /temp/requirements.txt
RUN apk add build-base libpq postgresql-dev && \
    pip install  -r /temp/requirements.txt


ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1


COPY django-blog /django-blog


WORKDIR /django-blog
EXPOSE 8000

RUN adduser --disabled-password blog-user

USER blog-user
