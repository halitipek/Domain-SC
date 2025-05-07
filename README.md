# Domain-SC: AI-Powered System Architecture Design

A comprehensive AI-powered system with enhanced RAG capabilities and multi-agent architecture for creating detailed software design documents.

[![Python Tests](https://github.com/halitipek/Domain-SC/actions/workflows/python-tests.yml/badge.svg)](https://github.com/halitipek/Domain-SC/actions/workflows/python-tests.yml)
[![Documentation Status](https://readthedocs.org/projects/domain-sc/badge/?version=latest)](https://domain-sc.readthedocs.io/en/latest/?badge=latest)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

Domain-SC is an advanced AI-powered system designed to generate detailed software architecture and design documents based on requirements. It leverages multiple specialized agents with enhanced RAG (Retrieval Augmented Generation) capabilities to produce high-quality, implementable software design specifications.

## Key Features

- **Enhanced RAG Capabilities**: Semantic pre-evaluation and smart caching optimize document retrieval
- **Optimized LLM Service**: Smart model selection based on task complexity
- **Adaptive Prompt System**: Performance tracking and template optimization
- **Simulation-Based Architecture Design**: Pre-simulation of designs ensures quality
- **Multi-Agent System**: Specialized agents for each aspect of the design process
- **Comprehensive CLI**: Fully-featured command-line interface
- **Detailed Documentation Generation**: Produces complete software design documents

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Quick Install

```bash
# Clone the repository
git clone https://github.com/halitipek/Domain-SC.git
cd Domain-SC

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# For development, install dev dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks (for development)
pre-commit install

# Make the CLI executable
chmod +x domain-sc
```

## Quick Start

Generate your first architecture document:

```bash
# Set up the demo environment
./domain-sc demo setup

# Run a sample workflow
./domain-sc demo workflow

# Or run a quick demo with custom requirements
./domain-sc demo quickstart --requirements "Create a scalable e-commerce system"
```

## Usage

### Command Line Interface

Domain-SC provides a comprehensive CLI for all operations:

```bash
# Get help
./domain-sc --help

# RAG commands
./domain-sc rag index -f resources/architecture_patterns.md -c architecture
./domain-sc rag query -q "What is microservices architecture?"

# Workflow commands
./domain-sc workflow create -n my_project -f requirements.md tech_constraints.md
./domain-sc workflow status -w workflow_id

# LLM commands
./domain-sc llm generate -p "Explain REST architecture"
./domain-sc llm templates

# Demo commands
./domain-sc demo enhanced -i requirements.md -o output_dir
```

See [docs/guides/cli-reference.md](docs/guides/cli-reference.md) for detailed CLI documentation.

## Project Structure

```
/Domain-SC
├── data/                   # Data storage (vector DB, outputs)
├── docs/                   # Documentation
│   ├── api/                # API reference
│   ├── guides/             # User guides
│   └── development/        # Developer documentation
├── resources/              # Knowledge resources for RAG
├── src/
│   ├── agents/             # Agent implementations
│   ├── cli/                # CLI implementation
│   ├── config/             # Configuration
│   ├── models/             # Data models
│   ├── prompts/            # Prompt templates
│   ├── services/           # Core services
│   └── utils/              # Utility functions
├── tests/
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── functional/         # Functional tests
├── .github/                # GitHub workflows and templates
├── .pre-commit-config.yaml # Pre-commit hooks
├── domain-sc               # CLI executable
├── mkdocs.yml              # Documentation configuration
├── pyproject.toml          # Project configuration
├── requirements.txt        # Production dependencies
└── requirements-dev.txt    # Development dependencies
```

## Documentation

For complete documentation, visit [domain-sc.readthedocs.io](https://domain-sc.readthedocs.io/).

Key documentation files:

- [User Guide](USER_GUIDE.md): Comprehensive guide for using Domain-SC
- [Executive Summary](EXECUTIVE_SUMMARY.md): High-level overview of the system
- [Workflows](WORKFLOWS.md): Detailed system workflows
- [Architecture](ARCHITECTURE.md): System architecture and components
- [API Guide](CLI_GUIDE.md): API usage documentation

## Development

To contribute to Domain-SC, please follow our [contributing guidelines](docs/development/CONTRIBUTING.md).

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Build documentation
mkdocs build
```

## License

MIT