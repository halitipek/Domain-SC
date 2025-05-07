# Domain-SC User Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Installation & Setup](#installation--setup)
3. [Configuration](#configuration)
4. [Using Domain-SC](#using-domain-sc)
   - [Creating Requirements](#creating-requirements)
   - [Generating Architectures](#generating-architectures)
   - [Viewing Results](#viewing-results)
   - [Enhancing the Knowledge Base](#enhancing-the-knowledge-base)
5. [Advanced Features](#advanced-features)
   - [Customizing Templates](#customizing-templates)
   - [Optimization Settings](#optimization-settings)
   - [Integration Options](#integration-options)
6. [API Reference](#api-reference)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)
9. [Glossary](#glossary)

## Introduction

Domain-SC is an AI-powered system architecture design platform that transforms natural language requirements into comprehensive, well-structured system architectures. This guide will help you set up, configure, and use Domain-SC effectively.

### Key Features

- **Natural Language Requirements**: Describe your system in plain language
- **Knowledge-Enhanced Design**: Leverages best practices through RAG
- **Simulation Validation**: Ensures consistency and quality
- **Cost Optimization**: Reduces token usage and operational costs
- **Adaptive Learning**: Improves over time based on usage

### System Requirements

- Python 3.8 or higher
- 8GB RAM minimum (16GB recommended)
- OpenAI API key or Anthropic API key
- Internet connection for API access

## Installation & Setup

### Basic Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Domain-SC.git
   cd Domain-SC
   ```

2. Create and activate a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_openai_api_key" > .env
   echo "ANTHROPIC_API_KEY=your_anthropic_api_key" >> .env
   ```

### Docker Installation

For containerized deployment:

1. Build the Docker image:
   ```bash
   docker build -t domain-sc .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 --env-file .env domain-sc
   ```

## Configuration

Domain-SC can be configured through the following methods:

### Environment Variables

Key environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `ANTHROPIC_API_KEY`: Your Anthropic API key
- `DEFAULT_MODEL`: Default LLM model to use
- `ENABLE_CACHE`: Enable semantic caching (true/false)
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)

### Configuration Files

The main configuration files are:

- `src/config/config.py`: Core configuration settings
- `requirements.txt`: Dependency specifications
- `.env`: Environment-specific settings (not committed to version control)

### Example Configuration

```python
# config.py
LLM_CONFIG = {
    "default_model": "gpt-4.1-2025-04-14",
    "fallback_model": "gpt-3.5-turbo",
    "lightweight_model": "gpt-3.5-turbo",
    "api_type": "openai",
    "temperature": 0.7,
    "max_tokens": 4000,
    "cache_ttl": 3600  # 1 hour
}

RAG_SETTINGS = {
    "vector_db_path": "data/vectordb",
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "embedding_model": "all-MiniLM-L6-v2",
    "similarity_top_k": 5
}
```

## Using Domain-SC

### Creating Requirements

Requirements should be detailed text descriptions of the system you want to design. Effective requirements include:

1. **System Purpose**: Clear statement of what the system should accomplish
2. **Key Features**: List of critical functionality
3. **Performance Expectations**: Response times, user loads, etc.
4. **Constraints**: Budget, technology, time limitations, etc.

#### Example Requirement

```
We need a highly scalable e-commerce platform capable of handling 10,000 concurrent users during peak shopping periods. The system should provide personalized shopping experiences, integrate with multiple payment providers, and offer real-time inventory management.

Key features include:
- Product catalog with advanced search and filtering
- User accounts with purchase history and recommendations
- Shopping cart and checkout process
- Payment processing with multiple providers
- Order management and tracking
- Inventory management with alerts

Performance requirements:
- Page load times under 2 seconds
- 99.9% uptime
- Support for mobile and web interfaces

Constraints:
- Must be cloud-native
- PCI DSS compliance required
- Integration with existing ERP system
```

### Generating Architectures

To generate an architecture:

1. **Using the Demo Script**:
   ```bash
   python demo_enhanced_system.py
   ```
   
   This will use the sample requirements in the script.

2. **Using Your Own Requirements**:
   
   Edit the `demo_enhanced_system.py` file and modify the `sample_requirements` variable with your requirements text.

3. **Using the Python API**:
   ```python
   from src.services.optimized_llm_service import OptimizedLLMService
   from src.services.enhanced_rag_service import EnhancedRAGService
   from src.agents.enhanced_system_architect_agent import EnhancedSystemArchitectAgent
   
   # Initialize services
   llm_service = OptimizedLLMService()
   rag_service = EnhancedRAGService()
   architect = EnhancedSystemArchitectAgent()
   
   # Define requirements
   requirements = {
       "description": "E-commerce platform",
       "features": ["Product catalog", "User accounts", "Payment processing"],
       "performance": "10,000 concurrent users"
   }
   
   # Define constraints
   constraints = {
       "technology": "Cloud-native",
       "security": "PCI DSS compliance"
   }
   
   # Generate architecture
   architecture = architect.design_architecture(requirements, constraints)
   ```

### Viewing Results

Results are stored in the `data/output/demo_results` directory:

- `structured_requirements.json`: Analyzed and structured requirements
- `rag_results.json`: Knowledge retrieved from the RAG system
- `design_input.json`: Formatted input for the architecture agent
- `generated_architecture.json`: Complete architecture in JSON format
- `generated_architecture.md`: Human-readable architecture document

#### Example Output

The generated architecture contains:
- High-level overview
- Detailed component descriptions
- Interface definitions
- Data flow mappings
- Deployment recommendations

### Enhancing the Knowledge Base

To improve the quality of architectures, you can enhance the knowledge base:

1. **Adding Reference Documents**:
   
   Place architecture reference documents in the `resources/` directory. Supported formats:
   - Markdown (.md)
   - Text (.txt)
   
   Example:
   ```bash
   cp my_architecture_pattern.md resources/
   ```

2. **Running Knowledge Indexing**:
   
   The knowledge base is automatically indexed when running the demo. To explicitly index new documents:
   
   ```python
   from src.services.enhanced_rag_service import EnhancedRAGService
   
   rag_service = EnhancedRAGService()
   rag_service.index_documents(["resources/my_architecture_pattern.md"])
   ```

3. **Quality Guidelines for Knowledge Documents**:
   
   - Focus on architecture patterns and best practices
   - Use clear headings and structure
   - Include pros/cons of different approaches
   - Avoid proprietary information
   - Keep documents concise and focused

## Advanced Features

### Customizing Templates

The adaptive prompt system uses templates from `src/prompts/templates/enhanced/`. You can customize these templates:

1. **Template Structure**:
   
   Templates are YAML files with the following structure:
   ```yaml
   id: "template_id"
   agent_id: "SAA"
   prompt_type: "pattern_selection"
   version: "1.0"
   template: |
     Your template text here with {{variables}}
   ```

2. **Creating New Templates**:
   
   To create a new template:
   - Create a new YAML file in the templates directory
   - Follow the structure above
   - Register it in the adaptive prompt system

3. **Template Variables**:
   
   Templates support variable substitution:
   - `{{requirements}}`: System requirements
   - `{{constraints}}`: System constraints
   - `{{context}}`: Additional context
   - Custom variables can be defined

### Optimization Settings

You can adjust optimization settings in `src/config/config.py`:

1. **LLM Optimization**:
   
   ```python
   LLM_CONFIG = {
       "default_model": "gpt-4.1-2025-04-14",  # Primary model
       "fallback_model": "gpt-3.5-turbo",      # Fallback model
       "lightweight_model": "gpt-3.5-turbo",   # For pre-filtering
       "cache_ttl": 3600,                      # Cache lifetime in seconds
   }
   ```

2. **RAG Optimization**:
   
   ```python
   RAG_SETTINGS = {
       "chunk_size": 1000,            # Size of document chunks
       "chunk_overlap": 200,          # Overlap between chunks
       "similarity_top_k": 5,         # Number of documents to retrieve
       "min_relevance": 0.45          # Minimum relevance threshold
   }
   ```

3. **Agent Settings**:
   
   ```python
   AGENT_SETTINGS = {
       "default_timeout": 120,        # Timeout in seconds
       "max_retries": 3,              # Maximum retry attempts
       "debug_mode": False            # Enable debug output
   }
   ```

### Integration Options

Domain-SC can be integrated with other systems:

1. **CLI Integration**:
   
   Use the CLI script for batch processing:
   ```bash
   python cli.py --input requirements.txt --output architecture.json
   ```

2. **API Integration**:
   
   The system can be exposed as an API:
   ```bash
   uvicorn src.api.router:app --host 0.0.0.0 --port 8000
   ```
   
   Then access the API at:
   ```
   POST http://localhost:8000/v1/architecture/generate
   ```

3. **Custom Integrations**:
   
   You can integrate the core components into your own applications:
   ```python
   from src.agents.enhanced_system_architect_agent import EnhancedSystemArchitectAgent
   
   # Initialize your custom integration
   architect = EnhancedSystemArchitectAgent()
   
   # Use the agent in your application
   result = architect.design_architecture(your_requirements, your_constraints)
   ```

## API Reference

### EnhancedSystemArchitectAgent

```python
design_architecture(requirements: Dict[str, Any], constraints: Dict[str, Any] = None) -> Dict[str, Any]
```
- `requirements`: Dictionary with system requirements
- `constraints`: Dictionary with system constraints
- Returns: Complete architecture design

### OptimizedLLMService

```python
generate_text(prompt: str, task_complexity: str = "medium", use_cache: bool = True) -> str
```
- `prompt`: The prompt to send to the LLM
- `task_complexity`: "low", "medium", or "high"
- `use_cache`: Whether to use semantic caching
- Returns: Generated text

### EnhancedRAGService

```python
semantic_retrieval(query: str, min_relevance: float = 0.45) -> List[Dict[str, Any]]
```
- `query`: The search query
- `min_relevance`: Minimum relevance threshold (0-1)
- Returns: List of relevant documents

```python
index_documents(file_paths: List[str]) -> Dict[str, Any]
```
- `file_paths`: List of paths to documents
- Returns: Indexing result status

### AdaptivePromptSystem

```python
get_template(agent_id: str, prompt_type: str) -> Dict[str, Any]
```
- `agent_id`: The agent ID (e.g., "SAA")
- `prompt_type`: The type of prompt (e.g., "pattern_selection")
- Returns: The best template for the given criteria

## Troubleshooting

### Common Issues

1. **API Key Errors**:
   
   ```
   Error: Authentication error with OpenAI API
   ```
   
   Solution: Check your `.env` file and ensure the API key is correct.

2. **Import Errors**:
   
   ```
   ModuleNotFoundError: No module named 'src'
   ```
   
   Solution: Run from the project root directory or adjust your PYTHONPATH:
   ```bash
   export PYTHONPATH=$PYTHONPATH:/path/to/Domain-SC
   ```

3. **Vector Store Errors**:
   
   ```
   Error: Vector store not initialized
   ```
   
   Solution: Ensure the `data/vectordb` directory exists and has write permissions.

4. **LLM Service Errors**:
   
   ```
   Error: Request to OpenAI API timed out
   ```
   
   Solution: Check your internet connection and increase the timeout in `config.py`.

### Logging

Logs are stored in the `logs/` directory:
- `enhanced_demo.log`: Main demo log
- `llm_service.log`: LLM service log
- `rag_service.log`: RAG service log
- `system_architect_agent.log`: Agent log

To increase logging detail, adjust the log level in `config.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

### Getting Help

If you encounter issues:
1. Check the logs in the `logs/` directory
2. Consult this user guide's troubleshooting section
3. Check the GitHub issues for similar problems
4. Submit a new issue with detailed error information

## Best Practices

### Writing Effective Requirements

1. **Be Specific**: Clearly state what the system should do
2. **Be Comprehensive**: Include all key features and constraints
3. **Include Performance Metrics**: Specify expected load, response times, etc.
4. **Define User Types**: Describe the different users of the system
5. **Identify Integration Points**: List systems the new system must work with

### Optimizing RAG Performance

1. **Quality Over Quantity**: Add fewer, high-quality documents rather than many low-quality ones
2. **Organize Knowledge**: Structure documents with clear headings and sections
3. **Focus on Patterns**: Include architecture patterns and their applications
4. **Update Regularly**: Keep knowledge base updated with new best practices

### Getting the Best Results

1. **Start Simple**: Begin with core requirements and add detail
2. **Iterate**: Generate, review, refine, and regenerate
3. **Provide Context**: Include domain-specific information
4. **Specify Constraints**: Clearly define limitations and requirements
5. **Review Output**: Always review and validate the generated architecture

## Glossary

- **LLM**: Large Language Model, the AI technology powering text generation
- **RAG**: Retrieval-Augmented Generation, technique to enhance responses with retrieved knowledge
- **Semantic Caching**: Storing and retrieving responses based on meaning similarity
- **Simulation-Based Approach**: Using simulation to predict and validate outputs
- **Prompt Template**: Structured format for generating LLM prompts
- **Vector Store**: Database for storing and retrieving document embeddings
- **Embedding**: Numerical representation of text for similarity comparison
- **Token**: Basic unit of text processing in LLMs
- **Architecture Component**: Discrete functional unit in a system architecture
- **Interface**: Connection point between components