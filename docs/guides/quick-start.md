# Quick Start Guide

This guide will help you get started with Domain-SC quickly and generate your first architecture document.

## Prerequisites

Make sure you have Domain-SC installed. If not, follow the [Installation Guide](installation.md).

## Setup the Demo Environment

Before running your first architecture generation, set up the demo environment which includes sample files and knowledge resources:

```bash
./domain-sc demo setup
```

This creates:
- Sample requirements, technology constraints, and optimization goals files
- Knowledge resources for architectural patterns, API design, and database design
- Indexes the knowledge resources for RAG retrieval

## Run a Sample Workflow

To see Domain-SC in action with the provided sample files:

```bash
./domain-sc demo workflow
```

This runs a complete workflow:
1. Creates a workflow with the sample files
2. Runs requirements analysis
3. Performs technology analysis
4. Generates an architecture design
5. Exports the results

The output will be saved to the configured output directory.

## Generate an Architecture from Custom Requirements

To generate an architecture from your own requirements:

### Quick Single-Prompt Generation

For a quick demo with a simple text prompt:

```bash
./domain-sc demo quickstart --requirements "Create a document management system that can process multiple document formats, extract text with OCR, support search with natural language queries, and provide a REST API for integration. The system should be scalable, secure, and have high availability."
```

This will generate a simplified architecture overview.

### Full Workflow with Custom Files

For a more comprehensive workflow with your own files:

1. Create your requirements file (e.g., `my_requirements.md`)
2. Create your technology constraints file (e.g., `my_tech.md`)
3. Create your optimization goals file (e.g., `my_goals.md`)
4. Run a workflow with your files:

```bash
./domain-sc workflow create -n my_project -f my_requirements.md my_tech.md my_goals.md
```

This will create a workflow and return a workflow ID. Use this ID in subsequent commands:

```bash
# Get workflow status
./domain-sc workflow status -w <workflow_id>

# Advance to requirements analysis
./domain-sc workflow advance -w <workflow_id> -p requirements_analysis

# Send a task to the Requirements Analysis Agent
./domain-sc workflow task -w <workflow_id> -a RAA -t analyze_requirements -d "Analyze requirements" -j '{"documents": {"requirements": "Path to the requirements file"}}'

# Advance to technology analysis
./domain-sc workflow advance -w <workflow_id> -p technology_analysis

# Send a task to the Technology Analysis Agent
./domain-sc workflow task -w <workflow_id> -a TAA -t analyze_technology -d "Analyze technology constraints" -j '{"documents": {"technology": "Path to the technology file", "optimization": "Path to the optimization file"}}'

# Advance to architecture design
./domain-sc workflow advance -w <workflow_id> -p architecture_design

# Send a task to the System Architect Agent
./domain-sc workflow task -w <workflow_id> -a SAA -t create_architecture_document -d "Create architecture document" -j '{"document_type": "SADD", "input_documents": {"requirements": "Contents of requirements file", "technology": "Contents of technology file", "optimization": "Contents of optimization file"}}'

# Finalize the workflow
./domain-sc workflow finalize -w <workflow_id>
```

## Enhance Your Knowledge Base

To improve the quality of generated architectures, add more knowledge to the RAG system:

```bash
# Index additional architectural knowledge
./domain-sc rag index -f path/to/architecture_docs/*.md -c architecture

# Query the knowledge base to verify
./domain-sc rag query -q "What are the best practices for microservices architecture?"
```

## Run the Enhanced Demo

For a comprehensive demonstration of all enhanced features:

```bash
./domain-sc demo enhanced -i path/to/requirements.md -o path/to/output
```

This runs a complete workflow with enhanced RAG, optimized LLM services, and the simulation-based architecture design approach.

## Next Steps

- Learn about the [CLI Reference](cli-reference.md) for all available commands
- Read the [Architecture](../architecture/overview.md) documentation to understand the system components
- Explore the [API Reference](../api/services.md) for programmatic access
- Check out the [Advanced Usage](advanced.md) guide for more complex scenarios