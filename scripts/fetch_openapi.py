#!/usr/bin/env python
# SPDX-License-Identifier: GPL-3.0-or-later
"""Fetch Metabase OpenAPI JSON from a live instance or the public docs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import httpx


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=None, help="Metabase base URL")
    parser.add_argument("--api-key", default=None, help="Metabase API key")
    parser.add_argument(
        "--public-docs-url",
        default="https://www.metabase.com/docs/latest/api.json",
        help="Public Metabase OpenAPI JSON URL used when --base-url is omitted or live fetch fails",
    )
    parser.add_argument("--output", default="docs/openapi.json")
    args = parser.parse_args()

    output = Path(args.output)
    headers = {"X-API-Key": args.api_key} if args.api_key else {}

    if args.base_url:
        base_url = args.base_url.rstrip("/")
        candidate_paths = ["/api/docs/openapi.json", "/api/docs/swagger.json", "/api/docs"]

        with httpx.Client(base_url=base_url, timeout=30) as client:
            for path in candidate_paths:
                response = client.get(path, headers=headers)
                content_type = response.headers.get("content-type", "")
                if response.status_code < 400 and "json" in content_type:
                    payload = response.json()
                    if isinstance(payload, dict) and "paths" in payload:
                        output.parent.mkdir(parents=True, exist_ok=True)
                        output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
                        print(f"Wrote {output} from {base_url}{path}")
                        return 0

    response = httpx.get(args.public_docs_url, timeout=30)
    if response.status_code < 400 and "json" in response.headers.get("content-type", ""):
        payload = response.json()
        if isinstance(payload, dict) and "paths" in payload:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
            print(f"Wrote {output} from {args.public_docs_url}")
            return 0

    print(
        "Could not fetch OpenAPI JSON from the live instance or public docs.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
