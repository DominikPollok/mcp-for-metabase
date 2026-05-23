from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def load_diff_module():  # type: ignore[no-untyped-def]
    script = Path(__file__).resolve().parents[1] / "scripts" / "diff_api_registry.py"
    spec = spec_from_file_location("diff_api_registry", script)
    assert spec is not None
    assert spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_diff_registries_reports_added_removed_and_changed() -> None:
    module = load_diff_module()

    diff = module.diff_registries(
        {
            "get_api_dashboard": {
                "operation_id": "get_api_dashboard",
                "method": "GET",
                "path": "/api/dashboard",
                "safety_tier": "read",
            },
            "delete_api_card_id": {
                "operation_id": "delete_api_card_id",
                "method": "DELETE",
                "path": "/api/card/{id}",
                "safety_tier": "destructive",
            },
        },
        {
            "get_api_dashboard": {
                "operation_id": "get_api_dashboard",
                "method": "GET",
                "path": "/api/dashboard",
                "safety_tier": "admin",
            },
            "post_api_dashboard": {
                "operation_id": "post_api_dashboard",
                "method": "POST",
                "path": "/api/dashboard",
                "safety_tier": "safe-write",
            },
        },
    )

    assert diff["added"] == ["post_api_dashboard"]
    assert diff["removed"] == ["delete_api_card_id"]
    assert diff["changed"] == {
        "get_api_dashboard": {"safety_tier": {"old": "read", "new": "admin"}}
    }
