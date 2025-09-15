"""
Main entry point for the Doppler Setup Intelligence PoC. This script
orchestrates the full Look -> Recognize -> Ask -> Act loop.
"""

import os
from typing import Optional, List

from doppler_poc.detectors import detect_docker_compose, detect_node_monorepo
from doppler_poc.api_simulator import simulate_api_calls
from doppler_poc.config_generator import generate_doppler_yaml


def main() -> None:
    """
    Executes the main logic of the proof-of-concept.
    """
    print("🚀 Doppler Setup Intelligence PoC - Initializing...")
    current_path = os.getcwd()
    project_name = os.path.basename(current_path)

    configs: Optional[List[str]] = None
    detected_type: Optional[str] = None

    # LOOK & RECOGNIZE
    print(f"Scanning directory: {current_path}")
    docker_services = detect_docker_compose(current_path)
    if docker_services:
        configs = docker_services
        detected_type = "Docker Compose"
    else:
        node_packages = detect_node_monorepo(current_path)
        if node_packages:
            configs = node_packages
            detected_type = "Node.js Monorepo"

    if not detected_type or not configs:
        print("❌ No recognizable project structure found. Exiting.")
        return

    # ASK
    print(f"✅ Detected {detected_type} project.")
    print("\nProposed Doppler Structure:")
    print(f"  Project: {project_name}")
    print("  Configs:")
    for config in configs:
        print(f"    - {config}")

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
    simulate_api_calls(project_name, configs)

    yaml_content = generate_doppler_yaml(project_name, configs)
    output_filename = "doppler.yaml"
    try:
        with open(output_filename, "w") as f:
            f.write(yaml_content)
        print(f"✅ Successfully generated '{output_filename}'!")
        print("\nTo get started, run: doppler run -- <your_command>")

    except IOError as e:
        print(f"🔥 Error writing to file: {e}")


if __name__ == "__main__":
    main()