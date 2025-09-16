"""
This module simulates the API calls that would be needed to create
the project structure within Doppler. In a real implementation, this
would use the Doppler API client.
"""

from typing import List


def simulate_api_calls(project_name: str, config_names: List[str]) -> str:
    """
    Generates a formatted string simulating the Doppler API calls.

    This function outlines the logical sequence of operations:
    1. Check for an existing project.
    2. Create the project if it doesn't exist.
    3. Create each of the required configs within that project.

    Args:
        project_name: The name of the Doppler project to be created.
        config_names: A list of config names to create within the project.

    Returns:
        A formatted, multi-line string detailing the simulated API calls.
    """
    output: List[str] = []
    output.append(f"1. [dim]Check if project exists:[/] '{project_name}'")
    output.append(f"2. [green]Create Project:[/] '{project_name}'")
    output.append(f"   [dim]POST /v3/projects[/dim]")
    output.append(f"   [dim]BODY: {{'name': '{project_name}'}}[/dim]")

    for i, config_name in enumerate(config_names):
        output.append(f"{i+3}. [cyan]Create Config:[/] '{config_name}'")
        output.append(f"   [dim]POST /v3/projects/{project_name}/configs[/dim]")
        output.append(
            f"   [dim]BODY: {{'name': '{config_name}', 'project': '{project_name}'}}[/dim]"
        )

    return "\n".join(output)
