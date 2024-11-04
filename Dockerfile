FROM python:3.10-slim-buster as builder
WORKDIR app

RUN pip install poetry==1.9.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false && \
    poetry install --without dev --no-root

FROM python:3.10-slim-buster
WORKDIR /app/
COPY bet_maker ./bet_maker
