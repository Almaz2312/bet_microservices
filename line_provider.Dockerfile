FROM python:3.10-slim-buster as builder
WORKDIR /line_provider

RUN pip install --upgrade pip
RUN pip install poetry==1.8.4

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY pyproject.toml poetry.lock /line_provider/

RUN poetry config virtualenvs.create false && \
    poetry install --no-root

FROM python:3.10-slim-buster
WORKDIR /line_provider/

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . /line_provider/
