import json
import sys
import tempfile

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@pytest.mark.asyncio
async def test_stdio_mcp_protocol_discovery_and_structured_tool_call() -> None:
    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_for_metabase", "serve", "--transport", "stdio"],
        env={
            "METABASE_URL": "http://metabase.test",
            "METABASE_MCP_WRITE_MODE": "read-only",
        },
    )

    with tempfile.TemporaryFile(mode="w+") as errlog:
        async with (
            stdio_client(params, errlog=errlog) as (read, write),
            ClientSession(read, write) as session,
        ):
            await session.initialize()
            tools = await session.list_tools()
            resources = await session.list_resources()
            prompts = await session.list_prompts()
            result = await session.call_tool(
                "metabase_discover_operations",
                {"text": "dashboard", "method": "POST", "limit": 1},
            )

    assert {tool.name for tool in tools.tools} >= {
        "metabase_api_request",
        "metabase_discover_operations",
    }
    assert {str(resource.uri) for resource in resources.resources} >= {
        "metabase://api/coverage",
        "metabase://api/operations",
    }
    assert {prompt.name for prompt in prompts.prompts} >= {"build_dashboard"}
    assert result.isError is False
    assert result.structuredContent is not None
    assert result.structuredContent["operation_count"] == 600
    assert result.structuredContent["returned_count"] == 1
    text_payload = json.loads(result.content[0].text)
    assert text_payload["operations"][0]["method"] == "POST"
