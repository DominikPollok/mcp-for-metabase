#!/usr/bin/env python
# SPDX-License-Identifier: GPL-3.0-or-later
"""Validate package version metadata before CI packaging or a PyPI release."""

from __future__ import annotations

import argparse
import ast
import sys
import tomllib
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

PACKAGE_NAME = "mcp-for-metabase"


def load_project_version(path: Path) -> str:
    with path.open("rb") as file:
        project = tomllib.load(file).get("project", {})
    version = project.get("version")
    if not isinstance(version, str) or not version:
        raise ValueError(f"{path} does not define a non-empty project.version")
    return version


def load_module_version(path: Path) -> str:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(
            isinstance(target, ast.Name) and target.id == "__version__" for target in node.targets
        ):
            continue
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            return node.value.value
    raise ValueError(f"{path} does not define a string __version__")


def validate_versions(*, project_version: str, module_version: str, tag: str | None) -> None:
    if project_version != module_version:
        raise ValueError(
            "package versions differ: "
            f"pyproject.toml has {project_version!r}, __init__.py has {module_version!r}"
        )
    if tag is not None and tag != f"v{project_version}":
        raise ValueError(
            f"release tag {tag!r} does not match package version {project_version!r}; "
            f"tag the release as 'v{project_version}' or bump both version declarations first"
        )


def pypi_version_exists(*, package: str, version: str) -> bool:
    url = f"https://pypi.org/pypi/{quote(package)}/{quote(version)}/json"
    request = Request(url, headers={"Accept": "application/json"})
    try:
        with urlopen(request, timeout=15) as response:
            return response.status == 200
    except HTTPError as exc:
        if exc.code == 404:
            return False
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pyproject", type=Path, default=Path("pyproject.toml"))
    parser.add_argument(
        "--module-init", type=Path, default=Path("src/mcp_for_metabase/__init__.py")
    )
    parser.add_argument("--tag", help="Release tag, expected to be v<project.version>")
    parser.add_argument(
        "--require-unpublished",
        action="store_true",
        help="Fail if the project version is already published on PyPI.",
    )
    args = parser.parse_args()

    try:
        project_version = load_project_version(args.pyproject)
        module_version = load_module_version(args.module_init)
        validate_versions(
            project_version=project_version,
            module_version=module_version,
            tag=args.tag,
        )
        if args.require_unpublished and pypi_version_exists(
            package=PACKAGE_NAME,
            version=project_version,
        ):
            raise ValueError(
                f"{PACKAGE_NAME} {project_version} is already published on PyPI; "
                "bump the package version before tagging a new release"
            )
    except (OSError, ValueError, HTTPError) as exc:
        print(f"Release version validation failed: {exc}", file=sys.stderr)
        return 1

    print(f"Release version validation passed: {PACKAGE_NAME} {project_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
