# SPDX-License-Identifier: GPL-3.0-or-later
from typing import Any

from mcp_for_metabase.application.common import omit_none
from mcp_for_metabase.client import MetabaseClient


async def list_pulses(client: MetabaseClient) -> dict[str, Any]:
    return await client.request("GET", "/api/pulse", operation_id="get_api_pulse")


async def get_pulse(client: MetabaseClient, *, pulse_id: int) -> dict[str, Any]:
    return await client.request(
        "GET",
        "/api/pulse/{id}",
        operation_id="get_api_pulse_id",
        path_params={"id": pulse_id},
    )


async def create_pulse(
    client: MetabaseClient,
    *,
    name: str,
    cards: list[dict[str, Any]],
    channels: list[dict[str, Any]],
    skip_if_empty: bool = False,
    dry_run: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "POST",
        "/api/pulse",
        operation_id="post_api_pulse",
        body={
            "name": name,
            "cards": cards,
            "channels": channels,
            "skip_if_empty": skip_if_empty,
        },
        dry_run=dry_run,
    )


async def update_pulse(
    client: MetabaseClient,
    *,
    pulse_id: int,
    updates: dict[str, Any],
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "PUT",
        "/api/pulse/{id}",
        operation_id="put_api_pulse_id",
        path_params={"id": pulse_id},
        body=updates,
        dry_run=dry_run,
        confirm=confirm,
    )


async def delete_pulse_subscription(
    client: MetabaseClient,
    *,
    pulse_id: int,
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "DELETE",
        "/api/pulse/{id}/subscription",
        operation_id="delete_api_pulse_id_subscription",
        path_params={"id": pulse_id},
        dry_run=dry_run,
        confirm=confirm,
    )


async def list_bookmarks(client: MetabaseClient) -> dict[str, Any]:
    return await client.request("GET", "/api/bookmark", operation_id="get_api_bookmark")


async def create_bookmark(
    client: MetabaseClient,
    *,
    model: str,
    entity_id: int,
    dry_run: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "POST",
        "/api/bookmark/{model}/{id}",
        operation_id="post_api_bookmark_model_id",
        path_params={"model": model, "id": entity_id},
        dry_run=dry_run,
    )


async def delete_bookmark(
    client: MetabaseClient,
    *,
    model: str,
    entity_id: int,
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "DELETE",
        "/api/bookmark/{model}/{id}",
        operation_id="delete_api_bookmark_model_id",
        path_params={"model": model, "id": entity_id},
        dry_run=dry_run,
        confirm=confirm,
    )


async def update_bookmark_ordering(
    client: MetabaseClient,
    *,
    ordering: list[dict[str, Any]],
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "PUT",
        "/api/bookmark/ordering",
        operation_id="put_api_bookmark_ordering",
        body={"ordering": ordering},
        dry_run=dry_run,
        confirm=confirm,
    )


async def list_revisions(
    client: MetabaseClient,
    *,
    entity: str,
    entity_id: int,
) -> dict[str, Any]:
    return await client.request(
        "GET",
        "/api/revision/{entity}/{id}",
        operation_id="get_api_revision_entity_id",
        path_params={"entity": entity, "id": entity_id},
    )


async def revert_revision(
    client: MetabaseClient,
    *,
    entity: str,
    entity_id: int,
    revision_id: int,
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "POST",
        "/api/revision/revert",
        operation_id="post_api_revision_revert",
        body={"entity": entity, "id": entity_id, "revision_id": revision_id},
        dry_run=dry_run,
        confirm=confirm,
    )


async def list_timelines(client: MetabaseClient) -> dict[str, Any]:
    return await client.request("GET", "/api/timeline", operation_id="get_api_timeline")


async def get_timeline(client: MetabaseClient, *, timeline_id: int) -> dict[str, Any]:
    return await client.request(
        "GET",
        "/api/timeline/{id}",
        operation_id="get_api_timeline_id",
        path_params={"id": timeline_id},
    )


async def create_timeline(
    client: MetabaseClient,
    *,
    name: str,
    collection_id: int | None = None,
    default: bool | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    body = omit_none({"name": name, "collection_id": collection_id, "default": default})
    return await client.request(
        "POST",
        "/api/timeline",
        operation_id="post_api_timeline",
        body=body,
        dry_run=dry_run,
    )


async def update_timeline(
    client: MetabaseClient,
    *,
    timeline_id: int,
    updates: dict[str, Any],
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "PUT",
        "/api/timeline/{id}",
        operation_id="put_api_timeline_id",
        path_params={"id": timeline_id},
        body=updates,
        dry_run=dry_run,
        confirm=confirm,
    )


async def delete_timeline(
    client: MetabaseClient,
    *,
    timeline_id: int,
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "DELETE",
        "/api/timeline/{id}",
        operation_id="delete_api_timeline_id",
        path_params={"id": timeline_id},
        dry_run=dry_run,
        confirm=confirm,
    )


async def create_timeline_event(
    client: MetabaseClient,
    *,
    timeline_id: int,
    name: str,
    timestamp: str,
    description: str | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    body = omit_none(
        {
            "timeline_id": timeline_id,
            "name": name,
            "timestamp": timestamp,
            "description": description,
        }
    )
    return await client.request(
        "POST",
        "/api/timeline-event",
        operation_id="post_api_timeline_event",
        body=body,
        dry_run=dry_run,
    )


async def update_timeline_event(
    client: MetabaseClient,
    *,
    event_id: int,
    updates: dict[str, Any],
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "PUT",
        "/api/timeline-event/{id}",
        operation_id="put_api_timeline_event_id",
        path_params={"id": event_id},
        body=updates,
        dry_run=dry_run,
        confirm=confirm,
    )


async def delete_timeline_event(
    client: MetabaseClient,
    *,
    event_id: int,
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "DELETE",
        "/api/timeline-event/{id}",
        operation_id="delete_api_timeline_event_id",
        path_params={"id": event_id},
        dry_run=dry_run,
        confirm=confirm,
    )


async def list_segments(client: MetabaseClient) -> dict[str, Any]:
    return await client.request("GET", "/api/segment", operation_id="get_api_segment")


async def get_segment(client: MetabaseClient, *, segment_id: int) -> dict[str, Any]:
    return await client.request(
        "GET",
        "/api/segment/{id}",
        operation_id="get_api_segment_id",
        path_params={"id": segment_id},
    )


async def create_segment(
    client: MetabaseClient,
    *,
    body: dict[str, Any],
    dry_run: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "POST",
        "/api/segment",
        operation_id="post_api_segment",
        body=body,
        dry_run=dry_run,
    )


async def update_segment(
    client: MetabaseClient,
    *,
    segment_id: int,
    updates: dict[str, Any],
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "PUT",
        "/api/segment/{id}",
        operation_id="put_api_segment_id",
        path_params={"id": segment_id},
        body=updates,
        dry_run=dry_run,
        confirm=confirm,
    )


async def delete_segment(
    client: MetabaseClient,
    *,
    segment_id: int,
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "DELETE",
        "/api/segment/{id}",
        operation_id="delete_api_segment_id",
        path_params={"id": segment_id},
        dry_run=dry_run,
        confirm=confirm,
    )


async def list_documents(client: MetabaseClient) -> dict[str, Any]:
    return await client.request("GET", "/api/document", operation_id="get_api_document")


async def get_document(client: MetabaseClient, *, document_id: int) -> dict[str, Any]:
    return await client.request(
        "GET",
        "/api/document/{document-id}",
        operation_id="get_api_document_document_id",
        path_params={"document_id": document_id},
    )


async def create_document(
    client: MetabaseClient,
    *,
    body: dict[str, Any],
    dry_run: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "POST",
        "/api/document",
        operation_id="post_api_document",
        body=body,
        dry_run=dry_run,
    )


async def update_document(
    client: MetabaseClient,
    *,
    document_id: int,
    updates: dict[str, Any],
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "PUT",
        "/api/document/{document-id}",
        operation_id="put_api_document_document_id",
        path_params={"document_id": document_id},
        body=updates,
        dry_run=dry_run,
        confirm=confirm,
    )


async def delete_document(
    client: MetabaseClient,
    *,
    document_id: int,
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "DELETE",
        "/api/document/{document-id}",
        operation_id="delete_api_document_document_id",
        path_params={"document_id": document_id},
        dry_run=dry_run,
        confirm=confirm,
    )


async def copy_document(
    client: MetabaseClient,
    *,
    document_id: int,
    name: str | None = None,
    collection_id: int | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    body = omit_none({"name": name, "collection_id": collection_id})
    return await client.request(
        "POST",
        "/api/document/{from-document-id}/copy",
        operation_id="post_api_document_from_document_id_copy",
        path_params={"from_document_id": document_id},
        body=body,
        dry_run=dry_run,
    )


async def get_cache_config(client: MetabaseClient) -> dict[str, Any]:
    return await client.request("GET", "/api/cache", operation_id="get_api_cache")


async def update_cache_config(
    client: MetabaseClient,
    *,
    config: dict[str, Any],
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "PUT",
        "/api/cache",
        operation_id="put_api_cache",
        body=config,
        dry_run=dry_run,
        confirm=confirm,
    )


async def invalidate_cache(
    client: MetabaseClient,
    *,
    body: dict[str, Any] | None = None,
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "POST",
        "/api/cache/invalidate",
        operation_id="post_api_cache_invalidate",
        body=body or {},
        dry_run=dry_run,
        confirm=confirm,
    )


async def clear_cache(
    client: MetabaseClient,
    *,
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "DELETE",
        "/api/cache",
        operation_id="delete_api_cache",
        dry_run=dry_run,
        confirm=confirm,
    )
