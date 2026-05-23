from pydantic import SecretStr

from mcp_for_metabase.config import Settings, WriteMode


def test_settings_normalizes_base_url() -> None:
    settings = Settings(
        METABASE_URL="http://localhost:3000/",
        METABASE_API_KEY=SecretStr("secret"),
    )

    assert settings.base_url == "http://localhost:3000"
    assert settings.write_mode == WriteMode.READ_ONLY


def test_settings_builds_outbound_headers() -> None:
    settings = Settings(
        METABASE_URL="http://localhost:3000/",
        METABASE_HTTP_HEADERS_JSON={"X-Proxy-User": "agent"},
        METABASE_BASIC_AUTH_USERNAME="proxy",
        METABASE_BASIC_AUTH_PASSWORD=SecretStr("secret"),
    )

    assert settings.outbound_headers["X-Proxy-User"] == "agent"
    assert settings.outbound_headers["Authorization"] == "Basic cHJveHk6c2VjcmV0"
