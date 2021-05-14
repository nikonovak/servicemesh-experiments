FROM centos:7 as base

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN yum install -y python3 guicorn
RUN pip3 install gunicorn flask pymemcache

COPY . /app

WORKDIR /app

CMD gunicorn --bind 0.0.0.0:8080 wsgi:app
