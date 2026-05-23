#!/usr/bin/env python
# SPDX-License-Identifier: GPL-3.0-or-later
"""Bootstrap a disposable Metabase instance and write integration-test env vars."""

from __future__ import annotations

import argparse
import secrets
import time
from pathlib import Path
from typing import Any

import httpx


def wait_for_metabase(base_url: str, timeout_seconds: int) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            response = httpx.get(f"{base_url}/api/session/properties", timeout=10)
            if response.status_code < 500:
                payload = response.json()
                if isinstance(payload, dict):
                    return payload
        except (httpx.HTTPError, ValueError) as exc:
            last_error = exc
        time.sleep(2)
    raise RuntimeError(f"Metabase did not become ready within {timeout_seconds}s: {last_error}")


def create_session(
    *,
    base_url: str,
    properties: dict[str, Any],
    email: str,
    password: str,
) -> str:
    setup_token = properties.get("setup-token")
    if isinstance(setup_token, str) and setup_token:
        response = httpx.post(
            f"{base_url}/api/setup",
            json={
                "token": setup_token,
                "user": {
                    "first_name": "MCP",
                    "last_name": "Integration",
                    "email": email,
                    "password": password,
                    "site_name": "MCP Integration",
                },
                "prefs": {
                    "site_name": "MCP Integration",
                    "site_locale": "en",
                    "allow_tracking": False,
                },
                "database": None,
            },
            timeout=30,
        )
    else:
        response = httpx.post(
            f"{base_url}/api/session",
            json={"username": email, "password": password},
            timeout=30,
        )
    response.raise_for_status()
    session = response.json().get("id")
    if not isinstance(session, str) or not session:
        raise RuntimeError("Metabase did not return a session id")
    return session


def create_api_key(*, base_url: str, session_id: str, name: str) -> str:
    headers = {"X-Metabase-Session": session_id}
    groups_response = httpx.get(f"{base_url}/api/permissions/group", headers=headers, timeout=30)
    groups_response.raise_for_status()
    groups = groups_response.json()
    admin_group_id = None
    if isinstance(groups, list):
        for group in groups:
            if isinstance(group, dict) and group.get("magic_group_type") == "admin":
                admin_group_id = group.get("id")
                break
    if not isinstance(admin_group_id, int):
        raise RuntimeError("Could not find Metabase Administrators group")

    key_response = httpx.post(
        f"{base_url}/api/api-key",
        headers={**headers, "Content-Type": "application/json"},
        json={"name": name, "group_id": admin_group_id},
        timeout=30,
    )
    key_response.raise_for_status()
    api_key = key_response.json().get("unmasked_key")
    if not isinstance(api_key, str) or not api_key:
        raise RuntimeError("Metabase did not return an API key")
    return api_key


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://localhost:3000")
    parser.add_argument("--timeout-seconds", type=int, default=180)
    parser.add_argument("--email", default="mcp-integration@example.com")
    parser.add_argument("--password", default=None)
    parser.add_argument("--api-key-name", default="mcp integration test")
    parser.add_argument("--output-env", type=Path, default=Path(".metabase-test.env"))
    args = parser.parse_args()

    password = args.password or f"Mcp-{secrets.token_urlsafe(24)}-1"
    properties = wait_for_metabase(args.base_url, args.timeout_seconds)
    session_id = create_session(
        base_url=args.base_url,
        properties=properties,
        email=args.email,
        password=password,
    )
    api_key = create_api_key(
        base_url=args.base_url,
        session_id=session_id,
        name=args.api_key_name,
    )
    args.output_env.write_text(
        f"METABASE_URL={args.base_url}\nMETABASE_API_KEY={api_key}\n",
        encoding="utf-8",
    )
    print(f"Wrote {args.output_env}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
