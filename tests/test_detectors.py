"""
Unit tests for the project structure detectors.
"""

from pathlib import Path
from typing import List, Optional
import pytest

from doppler_poc.detectors import detect_docker_compose, detect_node_monorepo


def test_detects_docker_compose_services() -> None:
    """
    Tests that the detector finds and parses a docker-compose.yml file.
    """
    # Arrange
    sample_project_path = Path(__file__).parent.parent / "sample_projects" / "docker_compose_simple"
    expected_services: List[str] = ["web", "api", "worker"]

    # Act
    detected_services: Optional[List[str]] = detect_docker_compose(str(sample_project_path))

    # Assert
    assert detected_services is not None
    assert sorted(detected_services) == sorted(expected_services)


def test_detects_node_monorepo_packages() -> None:
    """
    Tests that the detector finds and parses a Node.js monorepo structure.
    """
    # Arrange
    sample_project_path = Path(__file__).parent.parent / "sample_projects" / "node_monorepo"
    expected_packages: List[str] = ["frontend", "backend"]

    # Act
    detected_packages: Optional[List[str]] = detect_node_monorepo(str(sample_project_path))

    # Assert
    assert detected_packages is not None
    assert sorted(detected_packages) == sorted(expected_packages)


def test_no_detection_in_empty_dir(tmpdir: pytest.TempPathFactory) -> None:
    """
    Tests that no project is detected in an empty directory.
    """
    # Arrange
    empty_dir = str(tmpdir)

    # Act
    docker_result = detect_docker_compose(empty_dir)
    node_result = detect_node_monorepo(empty_dir)

    # Assert
    assert docker_result is None
    assert node_result is None