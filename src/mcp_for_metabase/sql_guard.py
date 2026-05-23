# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from mcp_for_metabase.config import SqlGuardMode
from mcp_for_metabase.errors import SafetyError

READ_ONLY_START_TOKENS = {"select", "with", "explain", "show", "describe", "desc"}
BLOCKED_SQL_TOKENS = {
    "alter",
    "analyze",
    "attach",
    "begin",
    "call",
    "commit",
    "copy",
    "create",
    "deallocate",
    "declare",
    "delete",
    "detach",
    "do",
    "drop",
    "execute",
    "grant",
    "infile",
    "insert",
    "into",
    "kill",
    "listen",
    "load",
    "lock",
    "merge",
    "notify",
    "optimize",
    "outfile",
    "prepare",
    "refresh",
    "replace",
    "reset",
    "revoke",
    "rollback",
    "set",
    "truncate",
    "unlock",
    "unload",
    "update",
    "use",
    "vacuum",
}
COMMENT_MARKERS = ("--", "/*", "*/", "#")
STRING_LITERAL_RE = re.compile(
    r"('(?:''|[^'])*')|(\"(?:\"\"|[^\"])*\")|(`(?:``|[^`])*`)",
    re.DOTALL,
)
TOKEN_RE = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")


@dataclass(frozen=True, slots=True)
class SqlFragment:
    sql: str
    location: str
    require_read_only_start: bool


def enforce_sql_guard(
    *,
    mode: SqlGuardMode,
    operation_id: str | None,
    path: str,
    body: Any,
) -> None:
    if mode == SqlGuardMode.DISABLED or body is None:
        return

    fragments = list(extract_sql_fragments(body, operation_id=operation_id, path=path))
    for fragment in fragments:
        validate_sql_fragment(fragment)


def extract_sql_fragments(
    body: Any,
    *,
    operation_id: str | None = None,
    path: str = "",
) -> list[SqlFragment]:
    operation = (operation_id or "").lower()
    normalized_path = path.lower()
    snippet_context = (
        "native_query_snippet" in operation
        or "native-query-snippet" in normalized_path
        or "snippet" in operation
    )
    fragments: list[SqlFragment] = []

    def add(sql: Any, location: str, *, full_query: bool) -> None:
        if isinstance(sql, str) and sql.strip():
            fragments.append(
                SqlFragment(
                    sql=sql,
                    location=location,
                    require_read_only_start=full_query,
                ),
            )

    def walk(value: Any, location: str) -> None:
        if isinstance(value, dict):
            value_type = str(value.get("type", "")).lower()
            native = value.get("native")
            query = value.get("query")

            if isinstance(native, dict):
                add(native.get("query"), f"{location}.native.query", full_query=True)
            elif isinstance(native, str):
                add(native, f"{location}.native", full_query=True)

            if value_type == "native":
                if isinstance(query, dict):
                    add(query.get("query"), f"{location}.query.query", full_query=True)
                else:
                    add(query, f"{location}.query", full_query=True)

            if snippet_context:
                add(value.get("content"), f"{location}.content", full_query=False)

            for key, child in value.items():
                walk(child, f"{location}.{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, f"{location}[{index}]")

    walk(body, "body")
    return _deduplicate_fragments(fragments)


def validate_sql_fragment(fragment: SqlFragment) -> None:
    sql = fragment.sql.strip()
    if "\x00" in sql:
        _raise_blocked(fragment, "SQL contains a NUL byte")
    scrubbed = _strip_literals(sql)
    if ";" in scrubbed:
        _raise_blocked(fragment, "SQL statement separators are not allowed")
    if any(marker in scrubbed for marker in COMMENT_MARKERS):
        _raise_blocked(fragment, "SQL comments are not allowed")

    tokens = [token.lower() for token in TOKEN_RE.findall(scrubbed)]
    if not tokens:
        _raise_blocked(fragment, "SQL does not contain a recognizable statement")

    blocked = sorted({token for token in tokens if token in BLOCKED_SQL_TOKENS})
    if blocked:
        _raise_blocked(
            fragment,
            "SQL contains blocked mutation/admin keywords",
            blocked_keywords=blocked,
        )

    if fragment.require_read_only_start and tokens[0] not in READ_ONLY_START_TOKENS:
        _raise_blocked(
            fragment,
            "native SQL must start with a read-only statement",
            first_token=tokens[0],
        )


def _strip_literals(sql: str) -> str:
    return STRING_LITERAL_RE.sub("''", sql)


def _deduplicate_fragments(fragments: list[SqlFragment]) -> list[SqlFragment]:
    seen: set[tuple[str, str, bool]] = set()
    deduplicated: list[SqlFragment] = []
    for fragment in fragments:
        key = (fragment.sql, fragment.location, fragment.require_read_only_start)
        if key in seen:
            continue
        seen.add(key)
        deduplicated.append(fragment)
    return deduplicated


def _raise_blocked(fragment: SqlFragment, reason: str, **extra: Any) -> None:
    raise SafetyError(
        f"Native SQL blocked: {reason}",
        response_body={
            "location": fragment.location,
            "reason": reason,
            **extra,
        },
    )
