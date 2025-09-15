"""
This module is responsible for generating the contents of the
project-local `doppler.yaml` file based on the detected project structure.
"""

from typing import Dict, Any
import yaml

from doppler_poc.models import DetectedProject


def generate_doppler_yaml(project: DetectedProject) -> str:
    """
    Generates the string content for a doppler.yaml file.

    Args:
        project_name: The name of the Doppler project.
        configs: A list of config names to be included in the file.

    Returns:
        A string containing the formatted YAML content.
    """
    yaml_structure: Dict[str, Any] = {"setup": []}

    for config_name, path in zip(project.configs, project.paths):
        yaml_structure["setup"].append(
            {
                "project": project.project_name,
                "config": config_name,
                "path": path,
            }
        )
    
    # Use yaml.dump to ensure correct formatting, indentation, and quoting
    return yaml.dump(yaml_structure, sort_keys=False, default_flow_style=False)