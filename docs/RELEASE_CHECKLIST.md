# Release Checklist

Use this checklist for each public release.

## Before Tagging

- Confirm the release scope is reflected in `CHANGELOG.md`.
- Choose a version that has not already been published to PyPI, then bump `version` in
  `pyproject.toml` and `src/mcp_for_metabase/__init__.py`. The release workflow fails instead of
  attempting to republish an existing version.
- Refresh `docs/API_COVERAGE.md` only when the generated registry changes.
- Run the full check suite:

```bash
uv run ruff format --check .
uv run ruff check .
uv run mypy src
uv run pytest
uv run python scripts/check_release_version.py
docker compose config --quiet
```

- Confirm the release workflow exists and targets PyPI trusted publishing:

```bash
test -f .github/workflows/release.yml
```

- Run disposable live integration tests:

```bash
docker compose up -d postgres metabase
uv run python scripts/bootstrap_metabase_test_instance.py --output-env .metabase-test.env
set -a && . ./.metabase-test.env && set +a
uv run pytest tests/integration -q --no-cov
docker compose down -v
rm -f .metabase-test.env
```

- Confirm the CI compatibility matrix is green for supported Metabase Docker tags.

- Build and inspect distributions:

```bash
uv run python -m build
uv run twine check dist/*
```

- Install the built wheel in a clean virtual environment and run:

```bash
mcp-for-metabase --help
python -m mcp_for_metabase.healthcheck
```

## PyPI Trusted Publishing

- Configure a PyPI Trusted Publisher for this GitHub repository.
- Use workflow file `.github/workflows/release.yml`.
- Use a protected GitHub environment named `pypi`.
- Publish only from signed or maintainer-created version tags matching `v*`; the release workflow does not support manual branch publishing.

## Tag And Publish

```bash
VERSION=0.4.0
uv run python scripts/check_release_version.py --tag "v${VERSION}" --require-unpublished
git tag "v${VERSION}"
git push origin "v${VERSION}"
```

The release workflow requires the tag to equal `v` plus the package version in the tagged
commit, and checks that the version is not already present on PyPI before publishing.

After the release workflow completes, verify:

- The PyPI project page renders the README correctly.
- The package metadata shows `GPL-3.0-or-later`.
- `pipx run mcp-for-metabase` or installation in a clean venv resolves the expected version.
- The GitHub release links to the changelog and PyPI package.
