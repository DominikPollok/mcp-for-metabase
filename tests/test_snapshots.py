import pytest

from mcp_for_metabase.errors import RegistryError
from mcp_for_metabase.snapshots import SnapshotStore


def test_snapshot_store_saves_loads_and_lists(tmp_path) -> None:  # type: ignore[no-untyped-def]
    store = SnapshotStore(tmp_path)

    saved = store.save(
        {
            "entity_type": "dashboard",
            "entity_id": 12,
            "snapshot": {"id": 12, "name": "Revenue"},
            "source_request_id": "request-1",
        },
    )
    loaded = store.load(saved["snapshot_id"])
    listed = store.list()

    assert loaded["snapshot"] == {"id": 12, "name": "Revenue"}
    assert loaded["snapshot_path"].endswith(f"{saved['snapshot_id']}.json")
    assert listed == [
        {
            "snapshot_id": saved["snapshot_id"],
            "created_at": saved["created_at"],
            "entity_type": "dashboard",
            "entity_id": 12,
            "source_request_id": "request-1",
            "snapshot_path": saved["snapshot_path"],
        },
    ]


def test_snapshot_store_rejects_path_traversal(tmp_path) -> None:  # type: ignore[no-untyped-def]
    store = SnapshotStore(tmp_path)

    with pytest.raises(RegistryError):
        store.load("../outside")
