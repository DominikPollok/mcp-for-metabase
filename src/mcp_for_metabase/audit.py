# SPDX-License-Identifier: GPL-3.0-or-later
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import structlog

logger = structlog.get_logger(__name__)


class AuditLogger:
    """Append-only JSONL audit log for mutating Metabase requests."""

    def __init__(self, path: Path | None) -> None:
        self.path = path

    def record(self, event: dict[str, Any]) -> None:
        payload = {"timestamp": datetime.now(UTC).isoformat(), **event}
        logger.info("metabase_mutation", **payload)
        if self.path is None:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, sort_keys=True, default=str) + "\n")
