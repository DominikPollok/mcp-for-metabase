# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from mcp_for_metabase.errors import RegistryError


class SnapshotStore:
    """Durable JSON snapshot store used by rollback-capable MCP tools."""

    def __init__(self, directory: Path) -> None:
        self.directory = directory

    def save(self, snapshot: dict[str, Any]) -> dict[str, Any]:
        entity_type = snapshot.get("entity_type")
        if not isinstance(entity_type, str) or not entity_type:
            raise RegistryError("snapshot must contain an entity_type")

        snapshot_id = str(uuid4())
        record = {
            "snapshot_id": snapshot_id,
            "created_at": datetime.now(UTC).isoformat(),
            **snapshot,
        }
        path = self._path_for(snapshot_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = path.with_suffix(".tmp")
        temporary_path.write_text(
            json.dumps(record, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        temporary_path.replace(path)
        return {**record, "snapshot_path": str(path)}

    def load(self, snapshot_id: str) -> dict[str, Any]:
        self._validate_snapshot_id(snapshot_id)
        path = self._path_for(snapshot_id)
        if not path.exists():
            raise RegistryError(
                f"Unknown snapshot_id: {snapshot_id}",
                response_body={"snapshot_dir": str(self.directory)},
            )
        record = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(record, dict):
            raise RegistryError(f"Snapshot file is invalid: {path}")
        return {**record, "snapshot_path": str(path)}

    def list(self, *, limit: int = 50) -> list[dict[str, Any]]:
        if not self.directory.exists():
            return []
        records: list[dict[str, Any]] = []
        for path in sorted(self.directory.glob("*.json"), reverse=True):
            record = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(record, dict):
                continue
            records.append(
                {
                    "snapshot_id": record.get("snapshot_id"),
                    "created_at": record.get("created_at"),
                    "entity_type": record.get("entity_type"),
                    "entity_id": record.get("entity_id"),
                    "source_request_id": record.get("source_request_id"),
                    "snapshot_path": str(path),
                },
            )
            if len(records) >= limit:
                break
        return records

    def _path_for(self, snapshot_id: str) -> Path:
        self._validate_snapshot_id(snapshot_id)
        return self.directory / f"{snapshot_id}.json"

    @staticmethod
    def _validate_snapshot_id(snapshot_id: str) -> None:
        if not snapshot_id or "/" in snapshot_id or "\\" in snapshot_id or ".." in snapshot_id:
            raise RegistryError("snapshot_id must be a plain file-safe identifier")
