# Doppler Setup Intelligence (PoC)

An intelligent onboarding engine for the Doppler CLI that automatically detects project architecture and generates configuration in seconds.

**Objective:** Remove onboarding friction and reduce Time-to-Value from minutes/hours to under 90 seconds.

## Problem

Doppler's CLI setup creates significant friction for complex applications. Developers must manually:
- Read extensive documentation
- Identify services needing secrets  
- Run multiple CLI commands
- Create doppler.yaml files

This undermines the "Time to Wow" moment and slows Product-Led Growth.

## Solution

Transforms `doppler setup` into an intelligent assistant that inspects projects, detects architecture, and generates perfect configuration.

## Features

- **Automatic Detection:** Scans for docker-compose.yml and package.json workspaces
- **Smart Configuration:** Creates separate Doppler configs per service/package
- **Interactive Confirmation:** Shows plan and waits for approval before proceeding
- **YAML Generation:** Produces properly formatted doppler.yaml files

## Quick Start

```bash
# Clone and setup
git clone https://github.com/your-username/doppler-setup-intelligence-poc.git
cd doppler-setup-intelligence-poc
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Run from sample project
cd sample_projects/docker_compose_simple/
python ../../main.py
```

## Scope

**IN SCOPE:**
- Docker Compose detection
- Node.js monorepo support  
- doppler.yaml generation
- CLI experience

**OUT OF SCOPE:**
- Other languages (Go, Python, Ruby)
- Advanced configs (branches, custom naming)
- Kubernetes/Terraform/CI integration
- .env migration
