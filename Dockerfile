FROM ghcr.io/astral-sh/uv:bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_INSTALL_DIR=/python
ENV UV_PYTHON_PREFERENCE=only-managed

COPY ./.python-version ./
RUN uv python install

WORKDIR /app/

COPY ./pyproject.toml ./
COPY ./smart_time_test/ ./smart_time_test/
COPY ./.env ./

RUN uv sync --no-dev
RUN uv run --no-dev ./smart_time_test/manage.py migrate
RUN uv run --no-dev python ./smart_time_test/manage.py loaddata ./smart_time_test/data.json

FROM debian:bookworm-slim

WORKDIR /app/

COPY --from=builder --chown=python:python /python /python

COPY --from=builder --chown=app:app /app /app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

CMD ["python", "./smart_time_test/manage.py", "runserver", "0.0.0.0:8000"]