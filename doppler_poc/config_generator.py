"""
This module is responsible for generating the contents of the
project-local `doppler.yaml` file based on the detected project structure.
"""

from typing import List, TypedDict
import yaml


class ConfigEntry(TypedDict):
    """Type definition for a single config entry in the doppler.yaml setup."""
    project: str
    config: str
    path: str


class DopplerYamlStructure(TypedDict):
    """Type definition for the complete doppler.yaml structure."""
    setup: List[ConfigEntry]


def generate_doppler_yaml(project_name: str, configs: List[str]) -> str:
    """
    Generates the string content for a doppler.yaml file.

    Args:
        project_name: The name of the Doppler project.
        configs: A list of config names to be included in the file.

    Returns:
        A string containing the formatted YAML content.
    """
    yaml_structure: DopplerYamlStructure = {"setup": []}
    for config_name in configs:
        config_entry: ConfigEntry = {
            "project": project_name, 
            "config": config_name, 
            "path": f"./{config_name}"
        }
        yaml_structure["setup"].append(config_entry)
    
    # Use yaml.dump to ensure correct formatting, indentation, and quoting
    return yaml.dump(yaml_structure, sort_keys=False, default_flow_style=False)