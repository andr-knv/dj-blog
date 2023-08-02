FROM python:3.11-bookworm

RUN apt install -y libpq-dev 

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt /temp/requirements.txt

RUN pip install --upgrade pip; pip install  -r /temp/requirements.txt

RUN adduser --disabled-password blog-user
USER blog-user

COPY django-blog /django-blog
WORKDIR /django-blog

EXPOSE 8000
