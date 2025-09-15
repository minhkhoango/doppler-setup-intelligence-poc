"""
Defines the data structures used for passing information between modules.
"""

from dataclasses import dataclass
from typing import List
from enum import Enum, auto


class ProjectType(Enum):
    """Enumeration for the different types of projects we can detect."""
    DOCKER_COMPOSE = auto()
    NODE_MONOREPO = auto()


@dataclass
class DetectedProject:
    """A structured representation of a detected project."""
    project_type: ProjectType
    project_name: str
    configs: List[str]
    paths: List[str]