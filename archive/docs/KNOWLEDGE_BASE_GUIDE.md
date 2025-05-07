# Knowledge Base Building Guide

This guide explains how to build and maintain the knowledge base for the Domain-SC system using the provided tools.

## Overview

The `build_knowledge_base.py` script automates the collection of architectural knowledge from various sources:

1. GitHub repositories with architecture documentation
2. Technical articles from engineering blogs and websites
3. Official documentation from technology providers
4. Local document directories

The collected knowledge is processed, converted to markdown format, and indexed by the RAG system for use by the agents.

## Prerequisites

Before running the knowledge base builder, ensure you have the required packages:

```bash
pip install requests beautifulsoup4 markdown markdownify
```

For improved GitHub API rate limits, you can set a GitHub token:

```bash
export GITHUB_TOKEN=your_github_token
```

## Basic Usage

To build the knowledge base with the default configuration:

```bash
python build_knowledge_base.py
```

This will:
1. Download and process sources defined in `kb_config/kb_sources.json`
2. Save processed documents to the `resources/` directory
3. Automatically run the RAG indexing process

## Configuration

The knowledge sources are defined in `kb_config/kb_sources.json`. You can customize this file to add or remove sources.

### GitHub Repositories

Add architectural knowledge repositories:

```json
"github_repos": [
  {
    "url": "https://github.com/username/repo",
    "branch": "main",
    "subdirectory": "docs",
    "patterns": [".md$"]
  }
]
```

### Technical Articles

Add URLs for important architecture articles:

```json
"articles": [
  "https://martinfowler.com/articles/microservices.html",
  "https://12factor.net/"
]
```

### Documentation Sites

Add official documentation sites that contain architectural patterns:

```json
"docs_sites": [
  {
    "url": "https://docs.microsoft.com/en-us/azure/architecture/patterns/",
    "include_paths": ["/azure/architecture/patterns/"],
    "depth": 1
  }
]
```

### Local Documents

Add paths to local directories containing architectural documentation:

```json
"local_docs": [
  "/path/to/architecture/documents/"
]
```

## Advanced Options

The script supports several command-line options:

```bash
# Only process GitHub repositories
python build_knowledge_base.py --github-only

# Only process web articles
python build_knowledge_base.py --articles-only

# Only process documentation sites
python build_knowledge_base.py --docs-only

# Only process local documents
python build_knowledge_base.py --local-only

# Clean temporary files before processing
python build_knowledge_base.py --clean

# Force refresh of all sources, even if already processed
python build_knowledge_base.py --force-refresh

# Use a custom configuration file
python build_knowledge_base.py --config path/to/config.json

# Specify a custom resources directory
python build_knowledge_base.py --resources-dir path/to/resources
```

## Adding Domain-Specific Knowledge

To optimize the system for your specific domain:

1. Create a directory for your domain-specific documents:
   ```bash
   mkdir -p resources/domain_specific
   ```

2. Add your domain knowledge files (markdown preferred)

3. Update the configuration to include this directory:
   ```json
   "local_docs": [
     "resources/domain_specific/"
   ]
   ```

4. Run the knowledge base builder:
   ```bash
   python build_knowledge_base.py --local-only
   ```

## Maintaining the Knowledge Base

For optimal performance:

1. Regularly update the knowledge base with new architectural patterns and practices
2. Remove outdated or irrelevant information
3. Focus on high-quality sources with practical examples
4. Include domain-specific knowledge relevant to your projects

## Troubleshooting

Common issues and solutions:

- **Rate limiting errors**: If you encounter API rate limits, set a `GITHUB_TOKEN` or reduce the number of sources
- **Memory issues**: If processing large documents causes memory issues, try processing fewer sources at once
- **Download failures**: Check your network connection and the validity of URLs in your configuration
- **Processing errors**: Ensure the documents are in a supported format; the script works best with markdown and HTML

If issues persist, check the logs in `logs/knowledge_base_builder.log` for detailed error information.