# Changelog

All notable changes to this project will be documented in this file.

This project follows the spirit of [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and uses semantic versioning once public releases begin.

## [Unreleased]

### Added

- Nothing yet.

## [0.1.0] - 2026-05-23

### Added

- Initial MCP server for Metabase with stdio and Streamable HTTP transports.
- API-key auth with username/password session fallback.
- Read-only default safety policy with `safe-writes`, `all-writes`, `confirm=true`, and `dry_run` gates.
- Strict native SQL guard that blocks stacked statements, comments, mutation/admin keywords, and non-read-only native query starts by default.
- Generated Metabase API registry and generic `metabase_api_request` executor.
- Curated tools for discovery, search, metadata inspection, queries, collections, cards, dashboards, snippets, and permissions graph updates.
- Curated tools for users, API keys, public links, copies, card queries/exports, pulses, bookmarks, revisions, timelines, segments, documents, and cache operations.
- Durable rollback snapshot store and saved snapshot restore tools.
- MCP-native discovery resources, prompts, and stdio protocol test coverage.
- Live integration bootstrap script for disposable Metabase instances.
- CI gates for Python 3.12/3.13, registry freshness, Docker smoke tests, package checks, and Metabase compatibility tests for `v0.59.7`, `v0.60.6`, and `v0.61.2`.
- PyPI trusted-publishing release workflow.
- Docker, Docker Compose, CI, tests, docs, examples, and Codex agent skills.
