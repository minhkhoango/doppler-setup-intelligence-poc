"""
Unit tests for the project structure detectors.

This file is a critical part of the TDD (Test-Driven Development) process.
We write a failing test first to clearly define the desired behavior,
then we write the code to make the test pass.
"""

import os
from typing import List, Optional

# This import will work once you have the project structure set up.
from doppler_poc.detectors import detect_docker_compose


def test_detects_docker_compose_services() -> None:
    """
    This is the first failing test.

    **Objective for Day 2:** Make this test pass.

    It checks if the `detect_docker_compose` function can correctly find
    a `docker-compose.yml` file in a sample directory and extract the
    names of the services defined within it ("web" and "api").
    """
    # Arrange: Point to the sample project directory
    sample_project_path = os.path.join(
        os.path.dirname(__file__), "..", "sample_projects", "docker_compose_simple"
    )
    expected_services: List[str] = ["web", "api"]

    # Act: Run the detector function on that directory
    detected_services: Optional[List[str]] = detect_docker_compose(sample_project_path)

    # Assert: Verify the outcome
    # 1. The function should not return None, it should find the services.
    assert detected_services is not None, "Failed to detect any services. The function returned None."

    # 2. The detected service names should match the expected names.
    # We sort both lists to ensure the comparison is not affected by order.
    assert sorted(detected_services) == sorted(
        expected_services
    ), f"Detected services '{detected_services}' do not match expected '{expected_services}'."