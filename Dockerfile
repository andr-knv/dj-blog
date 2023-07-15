FROM python:3.11-alpine3.18

COPY requirements.txt /temp/requirements.txt
COPY django-blog /django-blog
WORKDIR /django-blog
EXPOSE 8000


RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password blog-user

USER blog-user
