# SPDX-License-Identifier: GPL-3.0-or-later
import base64
from enum import StrEnum
from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Transport(StrEnum):
    STDIO = "stdio"
    HTTP = "http"


class WriteMode(StrEnum):
    READ_ONLY = "read-only"
    SAFE_WRITES = "safe-writes"
    ALL_WRITES = "all-writes"


class SqlGuardMode(StrEnum):
    STRICT = "strict"
    DISABLED = "disabled"


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    metabase_url: str = Field(default="http://localhost:3000", alias="METABASE_URL")
    metabase_api_key: SecretStr | None = Field(default=None, alias="METABASE_API_KEY")
    metabase_username: str | None = Field(default=None, alias="METABASE_USERNAME")
    metabase_password: SecretStr | None = Field(default=None, alias="METABASE_PASSWORD")
    metabase_http_headers: dict[str, str] = Field(
        default_factory=dict,
        alias="METABASE_HTTP_HEADERS_JSON",
    )
    metabase_basic_auth_username: str | None = Field(
        default=None,
        alias="METABASE_BASIC_AUTH_USERNAME",
    )
    metabase_basic_auth_password: SecretStr | None = Field(
        default=None,
        alias="METABASE_BASIC_AUTH_PASSWORD",
    )
    metabase_mcp_transport: Transport = Field(
        default=Transport.STDIO, alias="METABASE_MCP_TRANSPORT"
    )
    metabase_mcp_write_mode: WriteMode = Field(
        default=WriteMode.READ_ONLY,
        alias="METABASE_MCP_WRITE_MODE",
    )
    metabase_mcp_audit_log: Path | None = Field(default=None, alias="METABASE_MCP_AUDIT_LOG")
    metabase_mcp_snapshot_dir: Path = Field(
        default=Path(".mcp-for-metabase/snapshots"),
        alias="METABASE_MCP_SNAPSHOT_DIR",
    )
    metabase_mcp_timeout: float = Field(default=30.0, alias="METABASE_MCP_TIMEOUT", gt=0)
    metabase_mcp_http_host: str = Field(default="127.0.0.1", alias="METABASE_MCP_HTTP_HOST")
    metabase_mcp_http_port: int = Field(default=8000, alias="METABASE_MCP_HTTP_PORT", ge=1)
    metabase_mcp_sql_guard_mode: SqlGuardMode = Field(
        default=SqlGuardMode.STRICT,
        alias="METABASE_MCP_SQL_GUARD_MODE",
    )

    @field_validator("metabase_http_headers", mode="before")
    @classmethod
    def empty_headers_are_empty_dict(cls, value: object) -> object:
        if value == "":
            return {}
        return value

    @model_validator(mode="after")
    def validate_auth(self) -> "Settings":
        has_key = bool(self.metabase_api_key and self.metabase_api_key.get_secret_value())
        has_session_creds = bool(
            self.metabase_username
            and self.metabase_password
            and self.metabase_password.get_secret_value(),
        )
        if not has_key and not has_session_creds:
            return self
        return self

    @property
    def base_url(self) -> str:
        return str(self.metabase_url).rstrip("/")

    @property
    def write_mode(self) -> WriteMode:
        return self.metabase_mcp_write_mode

    @property
    def transport(self) -> Literal["stdio", "http"]:
        return self.metabase_mcp_transport.value

    @property
    def sql_guard_mode(self) -> SqlGuardMode:
        return self.metabase_mcp_sql_guard_mode

    @property
    def outbound_headers(self) -> dict[str, str]:
        headers = dict(self.metabase_http_headers)
        if self.metabase_basic_auth_username and self.metabase_basic_auth_password:
            credentials = (
                f"{self.metabase_basic_auth_username}:"
                f"{self.metabase_basic_auth_password.get_secret_value()}"
            )
            encoded = base64.b64encode(credentials.encode("utf-8")).decode("ascii")
            headers["Authorization"] = f"Basic {encoded}"
        return headers
