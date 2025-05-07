# System Overview

This document provides a high-level overview of the Domain-SC system architecture, its core components, and how they interact.

## Architecture Overview

Domain-SC is built using a modular architecture with specialized components that work together to generate comprehensive software architecture documents. The system leverages advanced AI techniques including:

1. **Retrieval-Augmented Generation (RAG)** with semantic pre-evaluation
2. **Multi-agent collaboration** with specialized roles
3. **Optimized LLM service** with smart model selection
4. **Adaptive prompt system** with performance tracking
5. **Simulation-based architecture design** for enhanced consistency

![Domain-SC System Architecture](../assets/images/system_architecture.png)

## Core Components

### Enhanced RAG Service

The Enhanced RAG Service improves traditional RAG by adding semantic pre-evaluation of documents to filter irrelevant content before processing with large models. Key features:

- **Semantic pre-evaluation**: Uses lightweight models to assess document relevance
- **Relevance caching**: Caches relevance scores to improve performance
- **Optimized retrieval**: Retrieves only the most relevant context for queries
- **Vector database integration**: Stores and queries document embeddings

### Optimized LLM Service

The Optimized LLM Service intelligently selects the most appropriate model for each task based on complexity, cost, and performance requirements. Key features:

- **Smart model selection**: Chooses between models based on task complexity
- **Semantic caching**: Caches responses based on semantic similarity
- **Cost tracking**: Monitors token usage and costs
- **Failure simulation**: Pre-tests reliability of generated outputs

### Adaptive Prompt System

The Adaptive Prompt System manages and optimizes prompt templates based on performance metrics. Key features:

- **Template versioning**: Tracks multiple versions of prompts
- **Performance tracking**: Monitors success rates of templates
- **Template selection**: Chooses best templates based on historical performance
- **Structured templates**: Uses YAML format for better organization

### Multi-Agent System

The system uses multiple specialized agents that collaborate to generate comprehensive architecture documents:

- **Requirements Analysis Agent (RAA)**: Analyzes project requirements
- **Technology Analysis Agent (TAA)**: Analyzes technical constraints
- **System Architect Agent (SAA)**: Designs system architecture
- **Optimization Agent (OA)**: Develops optimization strategies
- **Orchestrator Agent (OA)**: Coordinates workflow between agents

### Workflow Service

The Workflow Service manages the overall process flow and coordinates the interactions between agents. Key features:

- **Workflow state management**: Tracks state across complex workflows
- **Task routing**: Directs tasks to appropriate agents
- **Result aggregation**: Collects and organizes agent outputs
- **Phase transitions**: Manages transitions between workflow phases

## Interaction Flow

1. **Input Processing**:
   - User provides requirements, constraints, and optimization goals
   - Documents are processed and indexed by the RAG system

2. **Requirements Analysis**:
   - Requirements Analysis Agent analyzes input documents
   - Structured requirements are produced with clear categories

3. **Technology Analysis**:
   - Technology Analysis Agent analyzes technical constraints
   - Compatible technology stacks and patterns are identified

4. **Architecture Design**:
   - System Architect Agent retrieves relevant architecture patterns via RAG
   - Simulation of designs ensures quality and consistency
   - Components, interfaces, and data flows are designed

5. **Document Generation**:
   - Final architecture document is assembled
   - Includes components, interfaces, data models, and implementation guidance

## Key Innovations

1. **Semantic Pre-Evaluation in RAG**:
   - Reduces token usage by filtering irrelevant documents
   - Improves accuracy by focusing on relevant context

2. **Simulation-Based Architecture Design**:
   - Pre-simulates design outcomes before finalizing
   - Validates architectural decisions against requirements
   - Improves consistency and quality of designs

3. **Smart Model Selection**:
   - Optimizes cost by using lighter models for simpler tasks
   - Uses more powerful models for complex reasoning

4. **Adaptive Prompt Templates**:
   - Improves over time based on performance metrics
   - Ensures consistent high-quality outputs

## Data Flow

![Domain-SC Data Flow](../assets/images/data_flow.png)

1. **Input Data**: User provides requirements and constraints
2. **Document Processing**: Documents are chunked and embedded
3. **Vector Storage**: Embeddings are stored in vector database
4. **Query Processing**: User queries trigger document retrieval
5. **Agent Execution**: Agents process retrieved documents
6. **Output Generation**: Architecture document is generated

## Technology Stack

Domain-SC is built using the following technologies:

- **Backend**: Python 3.8+
- **Vector Database**: ChromaDB
- **Embedding Models**: Various embedding models
- **LLM Integration**: Multiple LLM providers
- **CLI Framework**: Custom CLI implementation
- **Documentation**: MkDocs with Material theme
- **Testing**: Pytest
- **Development Tools**: Black, isort, flake8, mypy