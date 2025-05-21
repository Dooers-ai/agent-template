# dooers.ai / agent-template / python-stream

A Python application service template with tools for development, testing, and formatting.

## Installation

Install the UV package manager (choose one):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

wget -qO- https://astral.sh/uv/install.sh | sh
```

## Setup

Create and activate virtual environment:
```bash
# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate
```

Install project dependencies:

```bash
uv sync
```

## Usage

```bash
# Start the application
uv run poe start

# Run tests
uv run poe test

# Run linting checks
uv run poe check

# Format code
uv run poe format
```

