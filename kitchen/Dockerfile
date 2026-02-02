# Stage 1: Builder
FROM python:3.13-slim-bookworm AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./
COPY shared ./shared
COPY kitchen/pyproject.toml ./kitchen/pyproject.toml
RUN uv sync --frozen --no-dev --no-install-project --package kitchen
COPY kitchen ./kitchen

# Stage 2: Runtime
FROM python:3.13-slim-bookworm

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/shared /app/shared
COPY --from=builder /app/kitchen /app/kitchen

ENV APP_PORT=9020
CMD fastapi run kitchen/app.py --port $APP_PORT --host 0.0.0.0
