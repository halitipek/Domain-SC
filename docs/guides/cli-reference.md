# CLI Reference

Domain-SC provides a comprehensive command-line interface (CLI) for all operations. This document serves as a reference for all available commands and their options.

## Global Options

These options apply to all commands:

```
--help, -h             Show help message and exit
```

## Command Structure

The Domain-SC CLI uses a command group structure:

```
domain-sc <command-group> <command> [options]
```

Available command groups:

- `rag`: RAG-related commands
- `workflow`: Workflow-related commands
- `llm`: LLM-related commands
- `demo`: Demo-related commands

## RAG Commands

Commands for working with the Retrieval-Augmented Generation (RAG) system.

### Index Documents

Index documents for RAG retrieval:

```bash
domain-sc rag index --files FILE [FILE ...] [--collection COLLECTION] [--chunk-size SIZE] [--chunk-overlap OVERLAP]
```

Options:
- `--files, -f`: Files to index (required)
- `--collection, -c`: Collection name (default: "default")
- `--chunk-size`: Chunk size for document processing (default: 1000)
- `--chunk-overlap`: Chunk overlap size (default: 200)

Example:
```bash
domain-sc rag index -f resources/architecture_patterns.md resources/api_design.md -c architecture
```

### Query RAG

Query the RAG system:

```bash
domain-sc rag query --query QUERY [--collection COLLECTION] [--top-k TOP_K] [--no-pre-eval]
```

Options:
- `--query, -q`: Query string (required)
- `--collection, -c`: Collection to query (default: from config)
- `--top-k, -k`: Number of results to return (default: from config)
- `--no-pre-eval`: Disable semantic pre-evaluation

Example:
```bash
domain-sc rag query -q "What is microservices architecture?" -c architecture -k 3
```

### Get RAG Statistics

Get statistics about the RAG index:

```bash
domain-sc rag stats
```

### Clear RAG Index

Clear the RAG index:

```bash
domain-sc rag clear [--collection COLLECTION] [--all]
```

Options:
- `--collection, -c`: Collection to clear (default: from config)
- `--all, -a`: Clear all collections

Example:
```bash
domain-sc rag clear -c architecture
```

### Export RAG Collection

Export a RAG collection:

```bash
domain-sc rag export --collection COLLECTION --output OUTPUT
```

Options:
- `--collection, -c`: Collection to export (required)
- `--output, -o`: Output file path (required)

Example:
```bash
domain-sc rag export -c architecture -o exports/architecture.json
```

### Import RAG Collection

Import a RAG collection:

```bash
domain-sc rag import --input INPUT [--collection COLLECTION]
```

Options:
- `--input, -i`: Input file path (required)
- `--collection, -c`: Collection name (if different from source)

Example:
```bash
domain-sc rag import -i exports/architecture.json -c new_architecture
```

## Workflow Commands

Commands for working with workflows.

### Create Workflow

Create a new workflow:

```bash
domain-sc workflow create --name NAME --files FILE [FILE ...] [--output-dir OUTPUT_DIR]
```

Options:
- `--name, -n`: Workflow name (required)
- `--files, -f`: Input files for the workflow (required)
- `--output-dir, -o`: Output directory for workflow artifacts

Example:
```bash
domain-sc workflow create -n my_project -f requirements.md technology.md -o output/my_project
```

### List Workflows

List all workflows:

```bash
domain-sc workflow list
```

### Get Workflow Status

Get workflow status:

```bash
domain-sc workflow status --workflow-id WORKFLOW_ID
```

Options:
- `--workflow-id, -w`: Workflow ID (required)

Example:
```bash
domain-sc workflow status -w 1234-5678-90ab-cdef
```

### Advance Workflow

Advance workflow to next phase:

```bash
domain-sc workflow advance --workflow-id WORKFLOW_ID --phase PHASE
```

Options:
- `--workflow-id, -w`: Workflow ID (required)
- `--phase, -p`: Next phase name (required)

Example:
```bash
domain-sc workflow advance -w 1234-5678-90ab-cdef -p requirements_analysis
```

### Send Task

Send a task to an agent:

```bash
domain-sc workflow task --workflow-id WORKFLOW_ID --agent-id AGENT_ID --task-type TASK_TYPE --description DESCRIPTION [--input-file INPUT_FILE] [--input-json INPUT_JSON]
```

Options:
- `--workflow-id, -w`: Workflow ID (required)
- `--agent-id, -a`: Agent ID (required)
- `--task-type, -t`: Task type (required)
- `--description, -d`: Task description (required)
- `--input-file, -i`: JSON file containing input data
- `--input-json, -j`: Task input data (JSON string)

Example:
```bash
domain-sc workflow task -w 1234-5678-90ab-cdef -a RAA -t analyze_requirements -d "Analyze requirements" -i input.json
```

### Finalize Workflow

Finalize a workflow:

```bash
domain-sc workflow finalize --workflow-id WORKFLOW_ID [--output-dir OUTPUT_DIR]
```

Options:
- `--workflow-id, -w`: Workflow ID (required)
- `--output-dir, -o`: Output directory for finalized artifacts

Example:
```bash
domain-sc workflow finalize -w 1234-5678-90ab-cdef -o output/final
```

### Export Workflow Results

Export workflow results:

```bash
domain-sc workflow export --workflow-id WORKFLOW_ID --output-dir OUTPUT_DIR [--format FORMAT]
```

Options:
- `--workflow-id, -w`: Workflow ID (required)
- `--output-dir, -o`: Output directory (required)
- `--format, -f`: Output format (json, md, all) (default: all)

Example:
```bash
domain-sc workflow export -w 1234-5678-90ab-cdef -o exports/my_project -f md
```

## LLM Commands

Commands for working with LLMs.

### Generate Text

Generate text using the LLM:

```bash
domain-sc llm generate [--prompt PROMPT] [--model MODEL] [--temperature TEMP] [--max-tokens MAX_TOKENS] [--streaming]
```

Options:
- `--prompt, -p`: Prompt string (if not provided, will read from stdin)
- `--model, -m`: Model name (default: from config)
- `--temperature, -t`: Temperature (default: from config)
- `--max-tokens, -k`: Max tokens (default: from config)
- `--streaming, -s`: Enable streaming output

Example:
```bash
domain-sc llm generate -p "Explain microservices architecture" -m gpt-4 -t 0.7
```

### Generate with Template

Generate text using a prompt template:

```bash
domain-sc llm prompt --template TEMPLATE [--variables VARIABLES] [--vars-file VARS_FILE] [--model MODEL] [--temperature TEMP] [--max-tokens MAX_TOKENS] [--streaming]
```

Options:
- `--template, -t`: Template name (required)
- `--variables, -v`: Variables for the prompt (JSON string)
- `--vars-file, -f`: JSON file containing variables
- `--model, -m`: Model name (default: from config)
- `--temperature, -T`: Temperature (default: from config)
- `--max-tokens, -k`: Max tokens (default: from config)
- `--streaming, -s`: Enable streaming output

Example:
```bash
domain-sc llm prompt -t architecture_pattern -v '{"pattern":"microservices","complexity":"high"}'
```

### List Templates

List available prompt templates:

```bash
domain-sc llm templates [--template TEMPLATE] [--format FORMAT]
```

Options:
- `--template, -t`: Specific template to show details for
- `--format, -f`: Output format (json or text) (default: text)

Example:
```bash
domain-sc llm templates -t architecture_pattern -f json
```

### List Models

List available LLM models:

```bash
domain-sc llm models
```

### Benchmark Models

Benchmark LLM performance:

```bash
domain-sc llm benchmark [--models MODEL [MODEL ...]] [--prompt PROMPT] [--iterations ITERATIONS] [--output OUTPUT]
```

Options:
- `--models, -m`: Models to benchmark (default: from config)
- `--prompt, -p`: Prompt to use for benchmarking
- `--iterations, -i`: Number of iterations (default: 3)
- `--output, -o`: Output file for benchmark results

Example:
```bash
domain-sc llm benchmark -m gpt-3.5-turbo gpt-4 -i 5 -o benchmark_results.json
```

## Demo Commands

Commands for running demonstrations.

### Setup Demo

Set up the demo environment:

```bash
domain-sc demo setup [--resources-dir RESOURCES_DIR] [--sample-dir SAMPLE_DIR]
```

Options:
- `--resources-dir`: Directory for demo resources
- `--sample-dir`: Directory for sample files

Example:
```bash
domain-sc demo setup --resources-dir custom_resources --sample-dir custom_samples
```

### Run Sample Workflow

Run a sample workflow:

```bash
domain-sc demo workflow [--output-dir OUTPUT_DIR]
```

Options:
- `--output-dir, -o`: Output directory for results

Example:
```bash
domain-sc demo workflow -o output/sample_workflow
```

### Run Quick Demo

Run a quick demo with simplified output:

```bash
domain-sc demo quickstart [--requirements REQUIREMENTS]
```

Options:
- `--requirements, -r`: Custom requirements text (uses default if not provided)

Example:
```bash
domain-sc demo quickstart -r "Create a scalable e-commerce system with payment processing"
```

### Run Enhanced Demo

Run enhanced system demo:

```bash
domain-sc demo enhanced [--input-file INPUT_FILE] [--output-dir OUTPUT_DIR]
```

Options:
- `--input-file, -i`: Input requirements file
- `--output-dir, -o`: Output directory for results

Example:
```bash
domain-sc demo enhanced -i requirements.md -o output/enhanced_demo
```

## Environment Variables

The CLI behavior can be modified using environment variables:

- `DOMAIN_SC_LLM_MODEL`: Default LLM model to use
- `DOMAIN_SC_LLM_TEMPERATURE`: Default temperature for LLM generation
- `DOMAIN_SC_LLM_MAX_TOKENS`: Default max tokens for LLM generation
- `DOMAIN_SC_RAG_COLLECTION`: Default RAG collection name
- `DOMAIN_SC_RAG_TOP_K`: Default number of results to return from RAG
- `DOMAIN_SC_VECTORDB_PATH`: Path to store vector database
- `DOMAIN_SC_OUTPUT_PATH`: Path for output files
- `DOMAIN_SC_LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)
- `DOMAIN_SC_LOG_DIR`: Directory for log files