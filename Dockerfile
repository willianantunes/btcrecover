FROM python:3.12-bullseye

RUN apt update && apt install -y git && apt clean

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false --local

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root

COPY . ./
