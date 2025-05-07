# Installation Guide

This guide covers the installation process for Domain-SC.

## Prerequisites

Before installing Domain-SC, ensure you have the following:

- Python 3.8 or higher
- pip package manager
- Git (for cloning the repository)
- Virtual environment tool (recommended)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/halitipek/Domain-SC.git
cd Domain-SC
```

### 2. Set Up a Virtual Environment

It's recommended to use a virtual environment to avoid dependency conflicts:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

Install the required dependencies:

```bash
# Install production dependencies
pip install -r requirements.txt

# For development, also install development dependencies
pip install -r requirements-dev.txt
```

### 4. Make the CLI Executable

Make the CLI script executable:

```bash
# On Linux/macOS:
chmod +x domain-sc

# On Windows, you can use the script directly with Python:
# python domain-sc
```

### 5. Verify Installation

Verify that the installation was successful:

```bash
./domain-sc --help
```

You should see the help message for the Domain-SC CLI.

## Environment Configuration

Domain-SC can be configured using environment variables or a configuration file.

### Environment Variables

Key environment variables:

- `DOMAIN_SC_LLM_MODEL`: Default LLM model to use
- `DOMAIN_SC_LLM_TEMPERATURE`: Default temperature for LLM generation
- `DOMAIN_SC_RAG_COLLECTION`: Default RAG collection name
- `DOMAIN_SC_VECTORDB_PATH`: Path to store vector database
- `DOMAIN_SC_OUTPUT_PATH`: Path for output files
- `DOMAIN_SC_LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)

Example:

```bash
export DOMAIN_SC_LLM_MODEL="gpt-4"
export DOMAIN_SC_LOG_LEVEL="DEBUG"
```

### Configuration File

You can also create a configuration file at `~/.config/domain-sc/config.json`:

```json
{
  "llm": {
    "default_model": "gpt-4",
    "default_temperature": 0.7,
    "default_max_tokens": 1000
  },
  "rag": {
    "default_collection": "architecture",
    "default_top_k": 5,
    "vectordb_path": "/path/to/vectordb"
  },
  "workflow": {
    "output_path": "/path/to/output"
  },
  "logging": {
    "level": "INFO",
    "log_dir": "/path/to/logs"
  }
}
```

## Docker Installation

If you prefer to use Docker, you can use the provided Dockerfile and docker-compose.yml:

```bash
# Build and start the services
docker-compose up --build

# Run a command in the container
docker-compose run domain-sc ./domain-sc --help
```

## Troubleshooting

### Common Issues

#### Missing Dependencies

If you encounter errors about missing dependencies:

```bash
pip install -r requirements.txt
```

#### Permission Denied for CLI

If you get a "permission denied" error when trying to run the CLI:

```bash
chmod +x domain-sc
```

#### Vector Database Issues

If the RAG service fails to initialize:

```bash
# Ensure the vector database directory exists
mkdir -p data/vectordb

# Run the setup to initialize the database
./domain-sc demo setup
```

### Getting Help

If you encounter any issues not covered here, please:

1. Check the [FAQ](faq.md) for common questions
2. Search the [GitHub Issues](https://github.com/halitipek/Domain-SC/issues) for similar problems
3. Open a new issue if needed