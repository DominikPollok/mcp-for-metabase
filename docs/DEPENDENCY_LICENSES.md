# Dependency License Review

`mcp-for-metabase` is released under `GPL-3.0-or-later`. Runtime dependencies must be compatible with GPLv3 distribution.

## Current Direct Runtime Dependencies

The current direct runtime dependencies are expected to be permissive or otherwise GPL-compatible:

| Dependency | Observed license family |
| --- | --- |
| `httpx` | BSD-3-Clause |
| `jsonschema` | MIT |
| `mcp` | MIT |
| `pydantic` | MIT |
| `pydantic-settings` | MIT |
| `structlog` | MIT / Apache-2.0 |
| `tenacity` | Apache-2.0 |
| `typer` | MIT |

## Release Gate

Before publishing a release, run a dependency license audit against the locked environment. Block the release if a runtime dependency has a GPLv3-incompatible license or unclear redistribution terms.

Suggested commands:

```bash
python -m pip install pip-licenses
pip-licenses --from=mixed --with-license-file --packages httpx jsonschema mcp pydantic pydantic-settings structlog tenacity typer
```

Record any dependency changes in this file or in the release notes.
