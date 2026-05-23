from pydantic import SecretStr

from mcp_for_metabase.config import Settings, WriteMode


def test_settings_normalizes_base_url() -> None:
    settings = Settings(
        METABASE_URL="http://localhost:3000/",
        METABASE_API_KEY=SecretStr("secret"),
    )

    assert settings.base_url == "http://localhost:3000"
    assert settings.write_mode == WriteMode.READ_ONLY
