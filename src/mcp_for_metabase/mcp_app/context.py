# SPDX-License-Identifier: GPL-3.0-or-later
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from mcp_for_metabase.client import MetabaseClient
from mcp_for_metabase.config import Settings
from mcp_for_metabase.snapshots import SnapshotStore


@dataclass(frozen=True, slots=True)
class McpAppContext:
    settings: Settings

    async def with_client(
        self,
        fn: Callable[[MetabaseClient], Awaitable[dict[str, Any]]],
    ) -> dict[str, Any]:
        async with MetabaseClient(self.settings) as client:
            return await fn(client)

    def snapshot_store(self) -> SnapshotStore:
        return SnapshotStore(self.settings.metabase_mcp_snapshot_dir)
