# Integration Testing

Unit tests use mocked HTTP. Live integration tests exercise a real Metabase instance and are skipped unless credentials are provided.

## Run With Docker Compose

Start Metabase and the MCP server dependencies:

```bash
docker compose up --build metabase postgres
```

Bootstrap a disposable admin user and API key:

```bash
uv run python scripts/bootstrap_metabase_test_instance.py --output-env .metabase-test.env
```

Run integration tests:

```bash
set -a
. ./.metabase-test.env
set +a
uv run pytest tests/integration -q --no-cov
```

The lifecycle test creates a collection, card, and dashboard, updates dashboard layout, snapshots the dashboard, then archives the created entities.

## Safety

Run integration tests against a disposable Metabase instance. The tests create and archive content and require an API key with content-write permissions.

Do not run the bootstrap script against a production Metabase instance. It creates an admin user during first setup and creates an Administrator API key for tests.
