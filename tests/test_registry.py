from mcp_for_metabase.registry import ApiRegistry, entries_from_openapi, operation_id_for


def test_default_registry_contains_dashboard_create() -> None:
    registry = ApiRegistry.load_default()

    operation = registry.get("post_api_dashboard")

    assert len(registry.operations) >= 500
    assert operation.method == "POST"
    assert operation.path == "/api/dashboard"
    assert operation.source_operation_id == "post-api-dashboard"
    assert operation.required_body_fields == ("name",)


def test_operation_id_for_normalizes_path() -> None:
    assert operation_id_for("GET", "/api/dashboard/{id}") == "get_api_dashboard_id"


def test_entries_from_openapi_classifies_operations() -> None:
    entries = entries_from_openapi(
        {
            "paths": {
                "/api/dashboard/{id}": {
                    "get": {"summary": "Get dashboard"},
                    "put": {"operationId": "putDashboard", "summary": "Update dashboard"},
                },
                "/api/permissions/graph": {
                    "put": {"summary": "Update permissions"},
                },
                "/api/dashboard/{dashboard-id}/dashcard/{dashcard-id}/execute": {
                    "post": {"summary": "Execute dashboard action"},
                },
            },
        },
    )

    by_id = {entry["operation_id"]: entry for entry in entries}
    assert by_id["get_api_dashboard_id"]["safety_tier"] == "read"
    assert by_id["putDashboard"]["safety_tier"] == "safe-write"
    assert by_id["put_api_permissions_graph"]["safety_tier"] == "admin"
    assert (
        by_id["post_api_dashboard_dashboard_id_dashcard_dashcard_id_execute"]["safety_tier"]
        == "admin"
    )
    assert by_id["putDashboard"]["required_body_fields"] == []


def test_registry_search_filters_by_tag_and_safety() -> None:
    registry = ApiRegistry.load_default()

    operations = registry.search(text="dashboard", tag="/api/dashboard", safety_tier=None, limit=5)

    assert operations
    assert all("/api/dashboard" in operation.tags for operation in operations)
