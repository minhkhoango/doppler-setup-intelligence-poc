"""
Contains the logic for detecting different project structures.

Each function in this module will be responsible for inspecting the file
system to identify a specific type of project (e.g., Docker Compose).
"""

from typing import List, Optional


def detect_docker_compose(path: str) -> Optional[List[str]]:
    """
    Detects if a docker-compose.yml file exists and extracts service names.

    Args:
        path: The directory path to scan.

    Returns:
        A list of service names if found, otherwise None.
    """
    # This is the function to be implemented on Day 2.
    # It currently does nothing, which will cause the unit test to fail.
    return None