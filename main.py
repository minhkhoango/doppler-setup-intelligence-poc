"""
Main entry point for the Doppler Setup Intelligence PoC. This script
orchestrates the full Look -> Recognize -> Ask -> Act loop.
"""

from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.prompt import Confirm

from doppler_poc.detectors import detect_project
from doppler_poc.api_simulator import simulate_api_calls
from doppler_poc.config_generator import generate_doppler_yaml
from doppler_poc.models import DetectedProject


def main() -> None:
    """
    Executes the main logic of the proof-of-concept.

    This function handles the user-facing presentation, confirmation flow,
    and orchestration of the backend logic (detection, generation, etc.).
    """
    console = Console()
    console.print(
        Panel(
            "[bold cyan]Doppler Setup Intelligence (PoC)[/bold cyan]",
            title="🚀 Initializing",
            border_style="green",
        )
    )
    current_path = Path.cwd()

    # --- 1. LOOK & RECOGNIZE ---
    with console.status(
        f"Scanning for project structure in [yellow]{current_path}[/yellow]..."
    ):
        detected_project: DetectedProject | None = detect_project(current_path)

    if not detected_project:
        console.print(
            "[bold red]❌ Error:[/bold red] No recognizable project structure found. Exiting."
        )
        return

    # --- 2. ASK ---
    # Build a readable summary of the proposed changes for the user.
    proposal = f"[bold]Project:[/bold] {detected_project.project_name}\n"
    proposal += "[bold]Configs:[/bold]\n"
    for config, path in zip(detected_project.configs, detected_project.paths):
        proposal += f"  - [cyan]{config}[/cyan] (path: [magenta]{path}[/magenta])"

    console.print(
        Panel(
            proposal,
            title="[yellow]Proposed Doppler Structure[/yellow]",
            border_style="blue",
            padding=(1, 2),
        )
    )

    # Use a rich Confirm prompt for a better UX than plain input().
    try:
        if not Confirm.ask("\n[bold]Proceed with this setup?[/bold]", default=True):
            console.print("[yellow]↪️ Setup cancelled by user. Exiting.[/yellow]")
            return
    except (KeyboardInterrupt):
        console.print("\n[yellow]↪️ Setup cancelled by user. Exiting.[/yellow]")
        return

    # --- 3. ACT ---
    console.print("\n[bold green]👍 Confirmation received. Starting setup...[/bold green]")
    
    # Simulate API calls and display them to the user.
    api_simulation_output = simulate_api_calls(
        detected_project.project_name, detected_project.configs
    )
    console.print(
        Panel(
            api_simulation_output,
            title="[yellow]API Call Simulation[/yellow]",
            border_style="dim blue",
        )
    )

    # Generate the YAML file.
    yaml_content = generate_doppler_yaml(detected_project)
    output_filepath = current_path / "doppler.yaml"

    try:
        output_filepath.write_text(yaml_content)
        console.print(
            f"[bold green]✅ Success:[/bold green] Generated '[bold cyan]{output_filepath.name}[/bold cyan]'!"
        )

        # Display the generated file with syntax highlighting.
        console.print(
            Panel(
                Syntax(yaml_content, "yaml", theme="monokai", line_numbers=True),
                title=f"Contents of {output_filepath.name}",
                border_style="green",
            )
        )
        console.print(
            "\n[bold]To get started, run: [cyan]doppler run -- <your_command>[/cyan][/bold]"
        )

    except IOError as e:
        console.print(f"[bold red]🔥 Error:[/bold red] Could not write to file: {e}")


if __name__ == "__main__":
    main()