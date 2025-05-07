# Domain-SC Architecture

This document provides a detailed overview of the Domain-SC architecture, focusing on how the different components interact with each other, particularly the RAG-enhanced System Architect Agent (SAA).

## System Components

The Domain-SC system consists of the following core components:

1. **Agent Framework**: A set of specialized agents for different aspects of system design
2. **RAG Service**: Provides knowledge retrieval and enhancement for agents
3. **Workflow Service**: Coordinates the multi-agent workflow process
4. **LLM Service**: Manages interactions with Large Language Models
5. **Prompt Management**: Structures and manages prompts for consistent agent outputs
6. **API Layer**: Exposes system functionality through REST endpoints

## Component Interaction Diagram

```
┌───────────────────────────────────────────────────────────────────────┐
│                             API Layer                                  │
└───────────────┬───────────────────┬────────────────────┬──────────────┘
                │                   │                    │
                ▼                   ▼                    ▼
┌──────────────────────┐ ┌───────────────────┐ ┌────────────────────────┐
│   Workflow Service   │ │    RAG Service    │ │      LLM Service       │
└─────────┬────────────┘ └─────────┬─────────┘ └───────────┬────────────┘
          │                        │                       │
          │                        │                       │
          │                        │   ┌───────────────────┐
          │                        │   │  Prompt Manager   │
          │                        │   └─────────┬─────────┘
          │                        │             │
          │                        │             │
┌─────────▼────────────────────────▼─────────────▼────────────────────────┐
│                                                                          │
│                              Agent Registry                              │
│                                                                          │
└──┬──────────┬──────────┬────────────┬──────────────┬──────────────┬─────┘
   │          │          │            │              │              │
   ▼          ▼          ▼            ▼              ▼              ▼
┌──────┐  ┌──────┐  ┌─────────┐  ┌─────────┐   ┌──────────┐   ┌──────────┐
│  OA  │  │ SAA  │  │   RAA   │  │   TAA   │   │    OAA   │   │  Other   │
│      │  │      │  │         │  │         │   │          │   │  Agents  │
└──────┘  └──┬───┘  └─────────┘  └─────────┘   └──────────┘   └──────────┘
            │
            ▼
  ┌─────────────────────┐
  │    RAG Context      │
  │    Enhancement      │
  └─────────────────────┘
```

## Agent Workflow Sequence

The following diagram shows the sequence of interactions in a typical workflow:

```
  Halit       Orchestrator   Document       Requirements    Technology      System
   (User)        Agent      Discovery Agent   Analysis      Analysis      Architect
     │             │             │               │             │              │
     │  initialize │             │               │             │              │
     │────────────>│             │               │             │              │
     │             │ delegate    │               │             │              │
     │             │─────────────>               │             │              │
     │             │             │               │             │              │
     │             │<╌╌╌╌╌╌╌╌╌╌╌╌╌               │             │              │
     │             │                             │             │              │
     │             │        advance to requirements phase      │              │
     │             │─────────────────────────────>             │              │
     │             │                             │             │              │
     │             │                    analyze requirements   │              │
     │             │                    with RAG assistance    │              │
     │             │<╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌             │              │
     │             │                                           │              │
     │             │             advance to technology phase   │              │
     │             │─────────────────────────────────────────>│              │
     │             │                                           │              │
     │             │                             analyze technology           │
     │             │                             with RAG assistance          │
     │             │<╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌              │
     │             │                                                          │
     │             │                   advance to architecture phase          │
     │             │─────────────────────────────────────────────────────────>│
     │             │                                                          │
     │             │                                      create architecture │
     │             │                                      with RAG enhancement│
     │             │<╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌│
     │             │                                                          │
     │  finalize   │                                                          │
     │────────────>│                                                          │
     │             │ collect all documents                                    │
     │             │─────────────────────────────────────────────────────────>│
     │             │                                                          │
     │<╌╌╌╌╌╌╌╌╌╌╌╌│                                                          │
     │  documents  │                                                          │
     │             │                                                          │
```

## RAG Enhancement for System Architect Agent

The System Architect Agent (SAA) is enhanced with Retrieval Augmented Generation (RAG) capabilities to improve its architecture design skills. Here's how the RAG enhancement process works:

```
┌────────────────────────────────────────────────────────────────────────────┐
│                         SAA RAG Enhancement Process                         │
└────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ 1. Query Enhancement                                                        │
│                                                                             │
│    Original Query: "How to design APIs for a distributed system?"           │
│                                                                             │
│    Enhanced Query: "system architecture design concepts for: How to design  │
│                     APIs for a distributed system?"                         │
└────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ 2. Knowledge Retrieval                                                      │
│                                                                             │
│    - Retrieve relevant documents from the vector database                   │
│    - Rank by similarity to the enhanced query                               │
│    - Select top k most relevant documents                                   │
└────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ 3. Prompt Construction                                                      │
│                                                                             │
│    - Get task-specific prompt template from Prompt Manager                  │
│    - Insert relevant context from retrieved documents                       │
│    - Add structured output expectations                                     │
└────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ 4. LLM Generation                                                           │
│                                                                             │
│    - Send enhanced prompt to LLM Service                                    │
│    - Set appropriate parameters (temperature, max_tokens)                   │
│    - Receive generated response                                             │
└────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ 5. Response Processing                                                      │
│                                                                             │
│    - Parse structured output                                                │
│    - Include source attribution                                             │
│    - Format according to expected output schema                             │
└────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

The following diagram shows how data flows through the system during architecture document creation:

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐     ┌──────────────┐
│  Input      │     │  Document    │     │  Vector       │     │ Architecture │
│  Documents  │────>│  Processor   │────>│  Database     │────>│ Knowledge    │
└─────────────┘     └──────────────┘     └───────────────┘     └──────────────┘
                                                                       │
                                                                       ▼
┌─────────────┐     ┌──────────────┐     ┌───────────────┐     ┌──────────────┐
│ Architecture│     │  System      │     │  LLM          │     │ Prompt       │
│ Document    │<────│  Architect   │<────│  Service      │<────│ Manager      │
└─────────────┘     └──────────────┘     └───────────────┘     └──────────────┘
```

## Key Benefits of the Architecture

1. **Specialized Agents**: Each agent focuses on a specific aspect of the system design process
2. **Knowledge-Enhanced Outputs**: RAG improves the quality of architectural documents
3. **Structured Process**: Clear workflow phases ensure a methodical approach
4. **Modular Design**: Components can be improved or replaced independently
5. **Consistent Outputs**: Prompt templates ensure consistent, well-structured outputs
6. **Efficient Resource Usage**: RAG enhances LLM capabilities while reducing token usage
7. **API-First Design**: All functionality is exposed through a clean API for integration

## Extension Points

The architecture is designed to be easily extensible in the following ways:

1. **New Agent Types**: Additional specialized agents can be added through the Agent Registry
2. **Custom Prompt Templates**: New templates can be added for different tasks
3. **Alternative LLM Providers**: The LLM Service abstracts provider-specific details
4. **Custom Workflow Phases**: The workflow process can be customized with new phases
5. **Additional RAG Knowledge**: The vector database can be expanded with new knowledge sources

## Knowledge Base Builder

Domain-SC includes advanced knowledge base building capabilities through two scripts:

1. **Basic Knowledge Base Builder**: `build_knowledge_base.py`
   - Downloads resources from various sources
   - Processes GitHub repositories, web articles, and documentation sites
   - Formats content for the RAG system

2. **Enhanced Knowledge Base Builder**: `enhanced_knowledge_base.py`
   - Adds semantic filtering to identify relevant content
   - Preserves relationships between documents in a network graph
   - Identifies architecture patterns across multiple categories:
     - Multi-agent systems patterns
     - General architecture patterns (layered, microservices, event-driven)
     - Design patterns (creational, structural, behavioral)
     - API design patterns
     - Data, security, and integration patterns
   - Extracts and categorizes code examples
   - Discovers additional relevant resources

To use the knowledge base builder:

```bash
# Basic usage
./build_knowledge_base.py

# Enhanced usage with resource discovery
./enhanced_knowledge_base.py --discover-resources
```

The knowledge base builders automatically populate the RAG system with architecture knowledge, improving the quality of the System Architect Agent's outputs.