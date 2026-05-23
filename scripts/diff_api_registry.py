#!/usr/bin/env python
# SPDX-License-Identifier: GPL-3.0-or-later
"""Compare two generated Metabase API registry JSON files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

COMPARE_FIELDS = (
    "method",
    "path",
    "safety_tier",
    "required_path_parameters",
    "required_query_parameters",
    "required_body_fields",
    "request_body_required",
    "deprecated",
)


def load_registry(path: Path) -> dict[str, dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError(f"{path} must contain a registry entry list")
    registry: dict[str, dict[str, Any]] = {}
    for entry in payload:
        if not isinstance(entry, dict) or not isinstance(entry.get("operation_id"), str):
            raise ValueError(f"{path} contains an invalid registry entry")
        registry[entry["operation_id"]] = entry
    return registry


def diff_registries(
    old: dict[str, dict[str, Any]],
    new: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    old_ids = set(old)
    new_ids = set(new)
    added = sorted(new_ids - old_ids)
    removed = sorted(old_ids - new_ids)
    changed: dict[str, dict[str, dict[str, Any]]] = {}
    for operation_id in sorted(old_ids & new_ids):
        field_changes: dict[str, dict[str, Any]] = {}
        for field in COMPARE_FIELDS:
            old_value = old[operation_id].get(field)
            new_value = new[operation_id].get(field)
            if old_value != new_value:
                field_changes[field] = {"old": old_value, "new": new_value}
        if field_changes:
            changed[operation_id] = field_changes
    return {
        "old_count": len(old),
        "new_count": len(new),
        "added": added,
        "removed": removed,
        "changed": changed,
    }


def render_markdown(diff: dict[str, Any]) -> str:
    lines = [
        "# API Registry Diff",
        "",
        f"- Old operations: {diff['old_count']}",
        f"- New operations: {diff['new_count']}",
        f"- Added: {len(diff['added'])}",
        f"- Removed: {len(diff['removed'])}",
        f"- Changed: {len(diff['changed'])}",
        "",
    ]
    for title, key in (("Added", "added"), ("Removed", "removed")):
        lines.extend([f"## {title}", ""])
        values = diff[key]
        if values:
            lines.extend(f"- `{operation_id}`" for operation_id in values)
        else:
            lines.append("- None")
        lines.append("")
    lines.extend(["## Changed", ""])
    if diff["changed"]:
        for operation_id, changes in diff["changed"].items():
            fields = ", ".join(f"`{field}`" for field in changes)
            lines.append(f"- `{operation_id}`: {fields}")
    else:
        lines.append("- None")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--old", required=True, type=Path)
    parser.add_argument("--new", required=True, type=Path)
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--fail-on-removal", action="store_true")
    args = parser.parse_args()

    diff = diff_registries(load_registry(args.old), load_registry(args.new))
    rendered = (
        json.dumps(diff, indent=2, sort_keys=True) + "\n"
        if args.format == "json"
        else render_markdown(diff)
    )
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    if args.fail_on_removal and diff["removed"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
