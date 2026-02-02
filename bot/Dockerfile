FROM python:3.13-slim-bookworm AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./
COPY shared ./shared
COPY bot/pyproject.toml ./bot/pyproject.toml
RUN uv sync --frozen --no-dev --no-install-project --package bot

COPY bot ./bot

FROM python:3.13-slim-bookworm

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/shared /app/shared
COPY --from=builder /app/bot /app/bot

CMD ["faststream", "run", "bot.app:app"]
