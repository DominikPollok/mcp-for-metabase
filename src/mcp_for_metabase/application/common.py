# SPDX-License-Identifier: GPL-3.0-or-later
from typing import Any


def omit_none(values: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in values.items() if value is not None}


def response_items(response: dict[str, Any]) -> list[Any]:
    data = response.get("data", [])
    if isinstance(data, dict):
        data = data.get("data", [])
    return data if isinstance(data, list) else []
