from mcp_for_metabase.redaction import redact_headers, redact_url


def test_redact_url_removes_userinfo() -> None:
    assert (
        redact_url("https://user:secret@metabase.example.com/api/collection/tree")
        == "https://metabase.example.com/api/collection/tree"
    )


def test_redact_headers_masks_authentication_headers() -> None:
    assert redact_headers({"Authorization": "Basic abc", "X-API-Key": "mb_key"}) == {
        "Authorization": "[REDACTED]",
        "X-API-Key": "[REDACTED]",
    }
