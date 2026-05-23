#!/usr/bin/env python
# SPDX-License-Identifier: GPL-3.0-or-later
"""Build the runtime Metabase API registry and coverage docs from OpenAPI."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mcp_for_metabase.registry import entries_from_openapi  # noqa: E402


def render_coverage(entries: list[dict[str, object]]) -> str:
    by_tier: dict[str, int] = {}
    for entry in entries:
        tier = str(entry["safety_tier"])
        by_tier[tier] = by_tier.get(tier, 0) + 1
    lines = [
        "# API Coverage",
        "",
        "This file is generated from the Metabase OpenAPI document.",
        "",
        f"- Total operations: {len(entries)}",
        *[f"- {tier}: {count}" for tier, count in sorted(by_tier.items())],
        "",
        "| Operation | Method | Path | Safety | Tags | Summary |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for entry in entries:
        render_entry = {
            key: ", ".join(value) if isinstance(value, list) else value
            for key, value in entry.items()
        }
        lines.append(
            "| {operation_id} | {method} | `{path}` | {safety_tier} | {tags} | {summary} |".format(
                **{key: str(value).replace("|", "\\|") for key, value in render_entry.items()},
            ),
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--openapi", default="docs/openapi.json")
    parser.add_argument("--registry", default="src/mcp_for_metabase/api_registry.json")
    parser.add_argument("--runtime-openapi", default="src/mcp_for_metabase/openapi.json")
    parser.add_argument("--coverage", default="docs/API_COVERAGE.md")
    args = parser.parse_args()

    openapi_path = Path(args.openapi)
    openapi = json.loads(openapi_path.read_text(encoding="utf-8"))
    entries = entries_from_openapi(openapi)

    registry_path = Path(args.registry)
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    registry_path.write_text(json.dumps(entries, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    runtime_openapi_path = Path(args.runtime_openapi)
    runtime_openapi_path.parent.mkdir(parents=True, exist_ok=True)
    runtime_openapi_path.write_text(
        json.dumps(openapi, separators=(",", ":"), sort_keys=True),
        encoding="utf-8",
    )

    coverage_path = Path(args.coverage)
    coverage_path.parent.mkdir(parents=True, exist_ok=True)
    coverage_path.write_text(render_coverage(entries), encoding="utf-8")

    print(
        f"Wrote {registry_path}, {runtime_openapi_path}, and {coverage_path} "
        f"with {len(entries)} operations",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
