"""
Main entry point for the Doppler Setup Intelligence PoC. This script
orchestrates the full Look -> Recognize -> Ask -> Act loop.
"""

from pathlib import Path

from doppler_poc.detectors import detect_project
from doppler_poc.api_simulator import simulate_api_calls
from doppler_poc.config_generator import generate_doppler_yaml
from doppler_poc.models import DetectedProject


def main() -> None:
    """
    Executes the main logic of the proof-of-concept.
    """
    print("🚀 Doppler Setup Intelligence PoC - Initializing...")
    current_path = Path.cwd()

    # LOOK & RECOGNIZE (Refactored)
    print(f"Scanning directory: {current_path}")
    detected_project: DetectedProject | None = detect_project(current_path)

    if not detected_project:
        print("❌ No recognizable project structure found. Exiting.")
        return

    # ASK
    print(f"✅ Detected {detected_project.project_type.name} project.")
    print("\nProposed Doppler Structure:")
    print(f"  Project: {detected_project.project_name}")
    print("  Configs:")
    for config, path in zip(detected_project.configs, detected_project.paths):
        print(f"    - {config} (path: {path})")

    try:
        confirm = input("\nProceed with this setup? (Y/n): ").lower().strip()
    except (EOFError, KeyboardInterrupt):
        print("\nAborted by user.")
        return

    if confirm not in ["y", "yes", ""]:
        print("❌ Setup cancelled by user. Exiting.")
        return

    # ACT
    print("\n👍 Confirmation received. Starting setup...")
    simulate_api_calls(detected_project.project_name, detected_project.configs)

    yaml_content = generate_doppler_yaml(detected_project)
    output_filepath = current_path / "doppler.yaml"
    try:
        output_filepath.write_text(yaml_content)
        print(f"✅ Successfully generated '{output_filepath.name}'!")
        print("\nTo get started, run: doppler run -- <your_command>")

    except IOError as e:
        print(f"🔥 Error writing to file: {e}")


if __name__ == "__main__":
    main()