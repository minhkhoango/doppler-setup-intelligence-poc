"""
Unit tests for the project structure detectors.
"""

from pathlib import Path
from doppler_poc.detectors import detect_project
from doppler_poc.models import ProjectType


def test_detects_docker_compose_project_correctly() -> None:
    """
    Tests that the detector finds, parses, and correctly structures
    a docker-compose.yml project.
    """
    # Arrange
    # Path(__file__) is the path to this test file. .parent gets the 'tests' dir.
    # .parent.parent gets the project root.
    sample_project_path = (
        Path(__file__).parent.parent / "sample_projects" / "docker_compose_simple"
    )
    expected_configs = ["web", "api", "worker"]

    # Act
    detected = detect_project(sample_project_path)

    # Assert
    assert detected is not None
    assert detected.project_type == ProjectType.DOCKER_COMPOSE
    assert detected.project_name == "docker_compose_simple"
    assert sorted(detected.configs) == sorted(expected_configs)
    assert detected.paths == ["./", "./", "./"]


def test_detects_node_monorepo_project_correctly() -> None:
    """
    Tests that the detector finds, parses, and correctly structures
    a Node.js monorepo project.
    """
    # Arrange
    sample_project_path = (
        Path(__file__).parent.parent / "sample_projects" / "node_monorepo"
    )
    expected_configs = ["frontend", "backend"]

    # Act
    detected = detect_project(sample_project_path)

    # Assert
    assert detected is not None
    assert detected.project_type == ProjectType.NODE_MONOREPO
    assert detected.project_name == "node_monorepo"
    assert sorted(detected.configs) == sorted(expected_configs)
    assert sorted(detected.paths) == sorted(
        ["./packages/backend", "./packages/frontend"]
    )


def test_no_detection_in_empty_dir(tmp_path: Path) -> None:
    """
    Tests that no project is detected in an empty directory.
    `tmp_path` is a pytest fixture that provides a temporary Path object.
    """
    # Act
    result = detect_project(tmp_path)

    # Assert
    assert result is None