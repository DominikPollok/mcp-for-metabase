FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN addgroup --system metabase-mcp && adduser --system --ingroup metabase-mcp metabase-mcp

COPY pyproject.toml README.md ./
COPY src ./src

RUN python -m pip install --upgrade pip && python -m pip install .

USER metabase-mcp

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -m mcp_for_metabase.healthcheck || exit 1

CMD ["mcp-for-metabase", "serve", "--transport", "http", "--host", "0.0.0.0", "--port", "8000"]
