# Domain-SC CLI Guide

The Domain-SC Command Line Interface (CLI) provides a convenient way to interact with the system from the command line. This guide explains how to use the CLI for common operations.

## Getting Started

Make sure you've installed all dependencies:

```bash
pip install -r requirements.txt
```

The CLI can be run with Python:

```bash
python cli.py [command] [subcommand] [options]
```

To see all available commands:

```bash
python cli.py --help
```

## Demo Commands

The quickest way to see the system in action is to use the demo commands:

### Set Up Demo Environment

Creates sample documents and architectural knowledge files, and sets up the RAG system:

```bash
python cli.py demo setup
```

### Run Sample Workflow

Runs a complete sample workflow including multiple agents:

```bash
python cli.py demo workflow
```

## RAG Commands

Commands for working with the RAG (Retrieval Augmented Generation) system:

### Index Documents

Add documents to the RAG index:

```bash
python cli.py rag index --files doc1.pdf doc2.md --collection my_collection
```

### Query the RAG System

Retrieve information from the RAG system:

```bash
python cli.py rag query --query "What is a microservices architecture?" --agent-type SAA --top-k 5
```

### Get RAG Statistics

View statistics about the RAG index:

```bash
python cli.py rag stats
```

### Clear the RAG Index

Remove all documents from the RAG index:

```bash
python cli.py rag clear
```

## Workflow Commands

Commands for managing multi-agent workflows:

### Create a Workflow

Start a new workflow with input files:

```bash
python cli.py workflow create --name my_workflow --files input1.pdf input2.md
```

### List Workflows

View all active workflows:

```bash
python cli.py workflow list
```

### Get Workflow Status

Check the status of a specific workflow:

```bash
python cli.py workflow status --workflow-id workflow_123
```

### Advance Workflow

Move a workflow to the next phase:

```bash
python cli.py workflow advance --workflow-id workflow_123 --phase requirements_analysis
```

### Send Task to Agent

Assign a task to a specific agent:

```bash
python cli.py workflow task --workflow-id workflow_123 --agent-id SAA --task-type create_architecture_document --description "Create SMAP" --input-data '{"document_type": "SMAP", "input_documents": {"requirements": "content"}}'
```

### Finalize Workflow

Complete a workflow and prepare deliverables:

```bash
python cli.py workflow finalize --workflow-id workflow_123
```

## LLM Commands

Commands for working with the LLM service:

### Generate Text

Generate text using the configured LLM:

```bash
python cli.py llm generate --prompt "Write a summary of microservices architecture" --model gpt-4 --temperature 0.7
```

You can also provide the prompt interactively:

```bash
python cli.py llm generate
```

### Generate with Agent Prompt

Generate text using an agent's prompt template:

```bash
python cli.py llm agent-prompt --agent-id SAA --prompt-type query_processing --variables '{"query": "What architecture pattern is best for a distributed system?"}'
```

### List Prompt Templates

View all available prompt templates:

```bash
python cli.py llm templates
```

Or view templates for a specific agent:

```bash
python cli.py llm templates --agent-id SAA
```

## Examples

### Complete Workflow Example

Here's an example of a complete workflow using the CLI:

```bash
# Set up the demo environment
python cli.py demo setup

# Create a new workflow
python cli.py workflow create --name architecture_design --files sample/sample_requirements.md sample/sample_technology.md

# Check the workflow ID from the output and use it in subsequent commands
WORKFLOW_ID="architecture_design_20250506_123456"

# Advance to requirements analysis
python cli.py workflow advance --workflow-id $WORKFLOW_ID --phase requirements_analysis

# Send a requirements analysis task
python cli.py workflow task --workflow-id $WORKFLOW_ID --agent-id RAA --task-type analyze_requirements --description "Analyze requirements" --input-data '{"documents": {"requirements": "sample content"}}'

# Advance to architecture design
python cli.py workflow advance --workflow-id $WORKFLOW_ID --phase architecture_design

# Send an architecture design task
python cli.py workflow task --workflow-id $WORKFLOW_ID --agent-id SAA --task-type create_architecture_document --description "Create SMAP" --input-data '{"document_type": "SMAP", "input_documents": {"requirements": "sample content"}}'

# Check workflow status
python cli.py workflow status --workflow-id $WORKFLOW_ID

# Finalize the workflow
python cli.py workflow finalize --workflow-id $WORKFLOW_ID
```

### RAG Example

Here's an example of working with the RAG system:

```bash
# Index some architecture documents
python cli.py rag index --files resources/architecture_patterns.md resources/api_design.md --collection architecture_knowledge

# Query the RAG system
python cli.py rag query --query "What are the benefits of microservices architecture?" --agent-type SAA --top-k 3

# Get statistics
python cli.py rag stats
```

## Advanced Usage

### Piping to/from Files

You can use Unix pipes to work with file contents:

```bash
# Index all markdown files in a directory
find resources/ -name "*.md" | xargs python cli.py rag index --collection docs

# Save RAG query results to a file
python cli.py rag query --query "microservices" > results.json

# Use a file as input for LLM generation
cat prompt.txt | python cli.py llm generate > response.txt
```

### Using Environment Variables

The CLI respects environment variables for API keys:

```bash
# Set API keys
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"

# Run CLI commands
python cli.py llm generate --prompt "Hello, world!"
```