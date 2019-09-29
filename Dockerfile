FROM python:alpine

RUN set -ex; \
  apk add gcc musl-dev libffi-dev openssl-dev python3-dev; \
  pip install python-telegram-bot; \
  apk del gcc;

WORKDIR /srv
