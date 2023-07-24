FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt /temp/requirements.txt

RUN pip install --upgrade pip; pip install  -r /temp/requirements.txt

COPY django-blog /django-blog


WORKDIR /django-blog
EXPOSE 8000

RUN adduser --disabled-password blog-user

USER blog-user
