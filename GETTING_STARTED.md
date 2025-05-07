# Getting Started with Domain-SC

This guide will help you set up and run the Domain-SC multi-agent system for architecture design, featuring the RAG-enhanced System Architect Agent.

## Prerequisites

- Python 3.8+ installed
- Pip package manager
- 4GB+ of RAM (for running the embedding models)
- Git (optional)

## Installation

### Option 1: Local Installation

1. Clone or download the repository:
   ```bash
   git clone https://github.com/yourusername/Domain-SC.git
   cd Domain-SC
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the RAG index with architecture knowledge:
   ```bash
   python src/setup.py --setup-rag
   ```

### Option 2: Docker Installation

1. Make sure Docker and Docker Compose are installed on your system.

2. Build and run the Docker container:
   ```bash
   docker-compose up --build
   ```

## Running the System

### Starting the API Server

```bash
python src/main.py
```

The API server will start on http://localhost:8000

### Running the Demo

To see a demonstration of the RAG-enhanced System Architect Agent:

```bash
python src/demo_rag.py
```

### Initializing a Sample Workflow

```bash
python src/setup.py --sample-workflow
```

This will:
1. Create sample input files
2. Initialize a workflow
3. Advance through multiple phases
4. Create architecture documents

## API Usage

The system exposes several API endpoints:

1. Check system status:
   ```bash
   curl http://localhost:8000/api/v1/status
   ```

2. Index documents for RAG:
   ```bash
   curl -X POST -H "Content-Type: application/json" \
     -d '{"file_paths": ["path/to/document1.md", "path/to/document2.pdf"]}' \
     http://localhost:8000/api/v1/documents/index
   ```

3. Query the RAG service:
   ```bash
   curl -X POST -H "Content-Type: application/json" \
     -d '{"query": "What architecture pattern is best for a distributed system?", "agent_type": "SAA"}' \
     http://localhost:8000/api/v1/rag/query
   ```

4. Get context for a specific agent:
   ```bash
   curl "http://localhost:8000/api/v1/context/SAA?query=How%20to%20design%20microservices"
   ```

## Project Organization

The project follows this structure:

```
/Domain-SC
├── data/               # Data storage for vector databases
├── logs/               # System logs
├── resources/          # Knowledge resources for RAG
├── sample/             # Sample input files for testing
├── src/
│   ├── agents/         # Agent implementations
│   ├── api/            # API endpoints
│   ├── config/         # Configuration
│   ├── models/         # Data models
│   ├── services/       # Core services
│   └── utils/          # Utility functions
```

## Key Configuration Options

Configuration is stored in `src/config/config.py`. Key settings include:

### RAG Settings

```python
RAG_SETTINGS = {
    "vector_db_path": os.path.join(BASE_DIR, "data", "vectordb"),
    "chunk_size": 500,
    "chunk_overlap": 50,
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "similarity_top_k": 5
}
```

### Agent Configuration

```python
SYSTEM_AGENTS = {
    "OA": {"name": "Orchestrator Agent", "max_tokens": 4000},
    "SAA": {"name": "System Architect Agent", "max_tokens": 8000},
    # Other agents...
}
```

## Custom Knowledge Integration

To add your own architectural knowledge to the RAG system:

1. Create markdown files with architecture information
2. Place them in the `resources/` directory
3. Run the indexing script:
   ```bash
   python src/setup.py --setup-rag --resource-dir ./resources
   ```

## Extending the System

### Adding New Agent Types

1. Create a new agent class in `src/agents/`
2. Inherit from `BaseAgent`
3. Implement specialized task execution methods
4. Register the agent type in the Workflow Service

### Adding New Document Types

Update the `DOCUMENT_LOADERS` dictionary in `src/utils/document_processor.py` to support additional file formats.

## Troubleshooting

### Vector Store Issues

If you encounter vector store errors:

```bash
# Clear the vector store
curl -X DELETE http://localhost:8000/api/v1/rag/clear

# Rebuild the index
python src/setup.py --setup-rag
```

### Agent Communication Issues

Check the logs in the `logs/` directory for detailed error information.