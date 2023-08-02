FROM python:3.11-bookworm

RUN apt update; apt upgrade -y;\
    apt install -y build-essential python3 python3-dev python3-pip  libpq-dev 

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt /temp/requirements.txt

RUN pip install --upgrade pip; pip install  -r /temp/requirements.txt

RUN adduser --disabled-password blog-user
USER blog-user

COPY django-blog /django-blog
WORKDIR /django-blog

EXPOSE 8000
