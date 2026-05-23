# Compatibility

Metabase’s REST API is not a stable versioned contract. This project tracks the latest public docs and validates against Dockerized Metabase versions.

Minimum compatibility policy:

- Latest Metabase release documented at https://www.metabase.com/docs/latest/api.
- Two previous supported Metabase Docker tags where practical.
- Changelog review for removed or changed endpoints before each release.

Registry compatibility workflow:

1. Fetch OpenAPI from the candidate Metabase version with `scripts/fetch_openapi.py`.
2. Build a temporary registry with `scripts/build_api_registry.py --registry /tmp/new_api_registry.json`.
3. Compare it to the packaged registry:

```bash
python scripts/diff_api_registry.py \
  --old src/mcp_for_metabase/api_registry.json \
  --new /tmp/new_api_registry.json \
  --format markdown \
  --fail-on-removal
```

Removed operations require a compatibility note, test update, and release note. Safety tier changes require review because they affect whether agents can mutate or administer content.

Known risk areas:

- MBQL serialization changes.
- Permissions graph shape changes.
- Notification and alert API transitions.
- Admin-only endpoints that require elevated Metabase groups.
