"""
This module simulates the API calls that would be needed to create
the project structure within Doppler. In a real implementation, this
would use the Doppler API client.
"""

from typing import List


def simulate_api_calls(project_name: str, config_names: List[str]) -> None:
    """
    Prints a simulation of the Doppler API calls.

    Args:
        project_name: The name of the Doppler project to be created.
        config_names: A list of config names to create within the project.
    """
    print("\n--- [API Call Simulation] ---")
    print(f"1. Check if project '{project_name}' exists...")
    print(f"2. Project does not exist. Creating project: '{project_name}'")
    print("   POST /v3/projects")
    print(f"   BODY: {{'name': '{project_name}'}}")
    for i, config_name in enumerate(config_names):
        print(f"{i+3}. Creating config: '{config_name}'")
        print(f"   POST /v3/projects/{project_name}/configs")
        print(f"   BODY: {{'name': '{config_name}', 'project': '{project_name}'}}")
    print("--- [End Simulation] ---\n")