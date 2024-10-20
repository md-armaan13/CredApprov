FROM python:3.14.0a1-alpine3.19
LABEL maintainer="mdarmaan13"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt


RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    adduser \
    --disabled-password \
    --no-create-home \
    appuser



COPY ./app app

WORKDIR /app

EXPOSE 8000

ENV PATH="/py/bin:$PATH"

USER appuser