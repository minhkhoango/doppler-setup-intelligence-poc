"""
Contains the logic for detecting different project structures.
These functions represent the work of Day 2 and Day 3.
"""

import json
from typing import List, Optional, Dict, Any
import yaml
from pathlib import Path


def detect_docker_compose(path: str) -> Optional[List[str]]:
    """
    Detects if a docker-compose.yml or docker-compose.yaml file exists
    and extracts the service names from it.

    Args:
        path: The directory path to scan.

    Returns:
        A list of service names if found, otherwise None.
    """
    for filename in ["docker-compose.yml", "docker-compose.yaml"]:
        compose_file_path = Path(path) / filename
        if compose_file_path.is_file():
            try:
                with open(compose_file_path, "r") as f:
                    compose_data: Dict[str, Any] = yaml.safe_load(f)
                    if compose_data and "services" in compose_data:
                        services = list(compose_data["services"].keys())
                        return services if services else None
            except (yaml.YAMLError, IOError):
                return None
    return None


def detect_node_monorepo(path: str) -> Optional[List[str]]:
    """
    Detects if a package.json indicates a Node.js monorepo (using workspaces)
    and extracts the package names.

    Args:
        path: The directory path to scan.

    Returns:
        A list of package directory names if found, otherwise None.
    """
    package_json_path = Path(path) / "package.json"
    if package_json_path.is_file():
        try:
            with open(package_json_path, "r") as f:
                package_data: Dict[str, Any] = json.load(f)
                if "workspaces" in package_data:
                    workspaces = package_data.get("workspaces", [])
                    if any("packages/*" in w for w in workspaces):
                        packages_dir = Path(path) / "packages"
                        if packages_dir.is_dir():
                            package_names: List[str] = [
                                p.name
                                for p in packages_dir.iterdir()
                                if p.is_dir()
                            ]
                            return package_names if package_names else None
        except (json.JSONDecodeError, IOError):
            return None
    return None