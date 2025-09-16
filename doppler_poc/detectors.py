"""
Contains the logic for detecting different project structures.
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any
import yaml

from doppler_poc.models import DetectedProject, ProjectType


def detect_project(path: Path) -> Optional[DetectedProject]:
    """
    Scans a directory and returns the first detected project type.

    Args:
        path: A Path object representing the directory to scan.
    """
    # .resolve() makes the path absolute, .name gets the final component
    project_name = path.resolve().name

    # Check for Docker Compose first
    for filename in ["docker-compose.yml", "docker-compose.yaml"]:
        compose_file_path = path / filename
        if compose_file_path.is_file():
            try:
                compose_data: Dict[str, Any] = yaml.safe_load(compose_file_path.read_text())
                if compose_data and "services" in compose_data:
                    services = list(compose_data["services"].keys())
                    if services:
                        return DetectedProject(
                            project_type=ProjectType.DOCKER_COMPOSE,
                            project_name=project_name,
                            configs=services,
                            # For Docker Compose, all paths are the root.
                            paths=["./" for _ in services],
                        )
            except (yaml.YAMLError, IOError):
                continue  # Try the next filename or detector

    # Check for Node.js Monorepo
    package_json_path = path / "package.json"
    if package_json_path.is_file():
        try:
            package_data: Dict[str, Any] = json.loads(package_json_path.read_text())
            if "workspaces" in package_data:
                # For this PoC, we assume a simple "packages/*" structure.
                workspaces = package_data.get("workspaces", [])
                if any("packages/*" in w for w in workspaces):
                    packages_dir = path / "packages"
                    if packages_dir.is_dir():
                        package_names = [
                            p.name for p in packages_dir.iterdir() if p.is_dir()
                        ]
                        if package_names:
                            return DetectedProject(
                                project_type=ProjectType.NODE_MONOREPO,
                                project_name=project_name,
                                configs=package_names,
                                # For Monorepos, paths are the package subdirectories.
                                paths=[f"./packages/{name}" for name in package_names],
                            )
        except (json.JSONDecodeError, IOError):
            pass  # Ignore errors and let it return None

    return None