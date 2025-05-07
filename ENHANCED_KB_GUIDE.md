# Enhanced Knowledge Base Guide

This guide explains how to use the enhanced knowledge base builder for Domain-SC.

## Features Overview

The `enhanced_knowledge_base.py` script provides advanced knowledge collection capabilities specifically designed for multi-agent systems architecture:

1. **Semantic Relevance Filtering**: Uses embeddings to assess content relevance to multi-agent systems
2. **Relationship Preservation**: Maintains link structure to understand document relationships
3. **Code Example Extraction**: Identifies and categorizes code examples of agent patterns
4. **Agent Pattern Recognition**: Automatically identifies common agent architecture patterns
5. **Resource Discovery**: Finds additional relevant resources from seed URLs

## Installation Requirements

```bash
pip install networkx numpy sentence-transformers requests beautifulsoup4 markdown markdownify
```

## Basic Usage

```bash
python enhanced_knowledge_base.py
```

This will:
1. Process sources from `kb_config/kb_sources.json`
2. Filter out irrelevant content
3. Extract code examples and identify patterns
4. Build a relationship graph of documents
5. Save everything to organized directories
6. Run the RAG indexing process

## Directory Structure

- `resources/`: Main processed documents with relevance filtering
- `kb_relationships/`: Relationship data between documents
- `kb_code_examples/`: Extracted code examples with pattern metadata
- `kb_config/`: Configuration and knowledge base reports

## Advanced Options

### Resource Discovery

To automatically discover additional relevant resources:

```bash
python enhanced_knowledge_base.py --discover-resources --max-discoveries 20
```

### Adjust Relevance Filtering

Control how strict the relevance filtering is:

```bash
python enhanced_knowledge_base.py --relevance-threshold 0.5  # More permissive (default is 0.65)
python enhanced_knowledge_base.py --relevance-threshold 0.8  # More strict
```

### Process Specific Source Types

```bash
# Only process GitHub repositories
python enhanced_knowledge_base.py --github-only

# Only process web articles
python enhanced_knowledge_base.py --articles-only

# Only process documentation sites 
python enhanced_knowledge_base.py --docs-only

# Only process local documents
python enhanced_knowledge_base.py --local-only
```

### Force Reprocessing

```bash
# Clean temp directory and force refresh all sources
python enhanced_knowledge_base.py --clean --force-refresh
```

## Understanding the Results

### Knowledge Report

A comprehensive report is generated at `kb_config/knowledge_report.json` with:
- Total documents processed
- Code examples extracted by pattern type
- Pattern coverage statistics
- Relationship graph metrics

### Relationship Graph

The relationship data is stored in `kb_relationships/knowledge_graph.json` and captures:
- Document relationships (which documents link to others)
- Document relevance scores
- Document titles and metadata

### Code Examples

Extracted code examples are saved in `kb_code_examples/code_examples.json` with:
- Code content
- Source information
- Language identification
- Detected agent patterns

## Identified Agent Patterns

The system automatically identifies these patterns in documents:

1. **Communication Protocols**: How agents exchange messages and data
2. **Coordination Mechanisms**: How agents work together
3. **State Management**: How agent state is maintained
4. **Task Allocation**: How work is distributed
5. **Failure Handling**: How errors and faults are managed

## Advanced Customization

### Adding Custom Pattern Types

Edit the `AGENT_PATTERNS` dictionary in the script to add new pattern types:

```python
AGENT_PATTERNS = {
    # Existing patterns...
    "your_new_pattern": [
        "keyword1", "keyword2", "phrase to match"
    ]
}
```

### Modifying Relevance Assessment

The reference text for determining relevance can be customized by editing the `MULTI_AGENT_REFERENCE` text in the script.

## Using Code Examples in Development

The extracted code examples can be directly used in your system implementation:

```python
import json

# Load code examples
with open('kb_code_examples/code_examples.json', 'r') as f:
    code_examples = json.load(f)

# Find examples of communication patterns
comm_examples = [ex for ex_id, ex in code_examples.items() 
                if 'communication_protocol' in ex.get('patterns', {})]

# Use examples in documentation
for ex in comm_examples[:3]:  # Top 3 examples
    print(f"Communication Pattern Example from {ex['source']}:")
    print(ex['code'])
    print("-" * 80)
```

## Troubleshooting

- **Missing semantic_model error**: Install sentence-transformers with `pip install sentence-transformers`
- **Rate limiting with GitHub**: Set GITHUB_TOKEN environment variable
- **Memory issues**: Reduce depth parameter for doc sites or process fewer sources
- **Network errors**: Check connection and try again with specific source types

For more help, check the log file at `logs/knowledge_base_builder.log`