from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest


def load_version_module():  # type: ignore[no-untyped-def]
    script = Path(__file__).resolve().parents[1] / "scripts" / "check_release_version.py"
    spec = spec_from_file_location("check_release_version", script)
    assert spec is not None
    assert spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_checked_in_package_versions_match() -> None:
    module = load_version_module()
    root = Path(__file__).resolve().parents[1]

    project_version = module.load_project_version(root / "pyproject.toml")
    package_version = module.load_module_version(root / "src/mcp_for_metabase/__init__.py")

    module.validate_versions(
        project_version=project_version,
        module_version=package_version,
        tag=f"v{project_version}",
    )


def test_rejects_out_of_sync_package_versions() -> None:
    module = load_version_module()

    with pytest.raises(ValueError, match="package versions differ"):
        module.validate_versions(project_version="0.4.0", module_version="0.3.0", tag=None)


def test_rejects_release_tag_without_version_bump() -> None:
    module = load_version_module()

    with pytest.raises(ValueError, match="does not match package version"):
        module.validate_versions(project_version="0.3.0", module_version="0.3.0", tag="v0.4.0")
