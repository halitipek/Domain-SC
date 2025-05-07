"""
Demo script showing the RAG enhancement for the System Architect Agent.
This demonstrates how the SAA now uses RAG to access architectural knowledge.
"""

import os
import sys
import asyncio
from pathlib import Path

# Add project root to Python path
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

# Check if we need to adjust the path
try:
    # First try importing normally
    from src.agents.system_architect_agent import SystemArchitectAgent
    from src.services.rag_service import RagService
    from src.utils.logger import setup_logger
    from src.models.base_models import AgentQuery
except ModuleNotFoundError:
    # If that fails, adjust the path and try again
    sys.path.append(str(root_dir))
    from agents.system_architect_agent import SystemArchitectAgent
    from services.rag_service import RagService
    from utils.logger import setup_logger
    from models.base_models import AgentQuery

# Set up logging
logger = setup_logger(__name__, "demo_rag.log")

async def setup_rag():
    """Set up the RAG system with sample architectural knowledge."""
    logger.info("Setting up RAG with sample knowledge")
    
    # Create resources directory
    resource_dir = root_dir / "resources"
    resource_dir.mkdir(exist_ok=True)
    
    # Create sample files with architecture knowledge
    create_architecture_knowledge_files(resource_dir)
    
    # Index files for RAG
    rag_service = RagService()
    files = [str(f) for f in resource_dir.glob("*.md") if f.is_file()]
    
    if files:
        result = rag_service.index_documents(files, collection_name="demo_knowledge")
        logger.info(f"Indexed {len(files)} knowledge files")
        return result
    else:
        logger.warning("No knowledge files found")
        return {"status": "warning", "message": "No knowledge files found"}

def create_architecture_knowledge_files(resource_dir):
    """Create sample files with architectural knowledge."""
    # Microservices architecture knowledge
    microservices_path = resource_dir / "microservices_architecture.md"
    if not microservices_path.exists():
        with open(microservices_path, 'w') as f:
            f.write("""# Microservices Architecture

## Overview
Microservices architecture is an architectural style that structures an application as a collection of small, loosely coupled services. Each service is focused on a specific business capability and can be developed, deployed, and scaled independently.

## Key Characteristics
1. **Service Independence**: Each service can be deployed independently
2. **Domain-Driven Design**: Services are organized around business domains
3. **Decentralized Data Management**: Each service manages its own database
4. **Smart Endpoints, Dumb Pipes**: Services communicate through simple protocols
5. **DevOps Culture**: Automated deployment and monitoring

## When to Use
- Large, complex applications with multiple teams
- Applications requiring different scaling needs for different components
- Systems needing frequent updates and independent deployments

## Challenges
- Increased operational complexity
- Distributed system challenges (network latency, fault tolerance)
- Data consistency across services
- Testing complexity
""")
            logger.info(f"Created knowledge file: {microservices_path}")
    
    # API Design knowledge
    api_path = resource_dir / "api_design_patterns.md"
    if not api_path.exists():
        with open(api_path, 'w') as f:
            f.write("""# API Design Patterns

## RESTful API Design
- Use HTTP methods appropriately (GET, POST, PUT, DELETE)
- Use nouns, not verbs, in endpoint paths
- Use plural nouns for collections
- Use status codes consistently
- Implement proper error handling
- Version your APIs

## GraphQL API Design
- Single endpoint for all resources
- Client specifies exactly what data it needs
- Strong typing system
- Introspection capabilities
- Efficient data loading

## API Gateway Pattern
- Single entry point for all clients
- Request routing
- Authentication and authorization
- Rate limiting and throttling
- Response caching
- API composition
""")
            logger.info(f"Created knowledge file: {api_path}")
    
    # Module Design knowledge
    module_path = resource_dir / "module_design_patterns.md"
    if not module_path.exists():
        with open(module_path, 'w') as f:
            f.write("""# Module Design Patterns

## Module Organization Patterns
- **Core-Satellite**: Central core module with peripheral satellites
- **Layered Architecture**: UI, business logic, data access layers
- **Feature-Based**: Modules organized by business feature
- **Domain-Driven**: Modules represent business domains

## Design Principles
- **High Cohesion**: Modules should have focused responsibilities
- **Low Coupling**: Minimize dependencies between modules
- **Information Hiding**: Expose minimal interfaces
- **Open-Closed Principle**: Open for extension, closed for modification

## Communication Patterns
- **Synchronous Communication**: Direct method calls or HTTP requests
- **Asynchronous Communication**: Message queues, event streams
- **Publisher-Subscriber**: Event-based communication
- **Request-Response**: Query-based communication
""")
            logger.info(f"Created knowledge file: {module_path}")

async def demo_rag_enhanced_saa():
    """Demonstrate the RAG-enhanced System Architect Agent."""
    # Create the System Architect Agent
    saa = SystemArchitectAgent()
    
    print("\n=== System Architect Agent with RAG Enhancement ===\n")
    
    # Simulate queries to the SAA that will benefit from RAG
    queries = [
        "What architecture pattern would you recommend for a distributed e-commerce system?",
        "How should we design the APIs for our microservices architecture?",
        "What's the best way to organize modules in our system to minimize dependencies?"
    ]
    
    for i, query_text in enumerate(queries):
        print(f"\nQuery {i+1}: {query_text}\n")
        
        # Create a query from another agent
        query = AgentQuery(
            query_id=f"demo_query_{i+1}",
            sender="RAA",  # Pretending to be the Requirements Analysis Agent
            recipient="SAA",
            content=query_text
        )
        
        # Process the query
        response = saa.process_query(query)
        
        # Display the response
        print("Response from SAA:")
        print("-" * 40)
        print(response.content)
        print("-" * 40)
        
        # Display sources (from RAG)
        if response.sources:
            print("\nSources used (from RAG):")
            for j, source in enumerate(response.sources):
                print(f"{j+1}. From: {source.get('source', 'unknown')}")
                print(f"   Content snippet: {source.get('content', '')[:100]}...")
        
        await asyncio.sleep(1)  # Pause between queries

async def main():
    """Main function to run the demo."""
    # Setup RAG with knowledge
    print("Setting up RAG with architectural knowledge...")
    setup_result = await setup_rag()
    print(f"RAG Setup Result: {setup_result['status']}")
    
    # Demo the RAG-enhanced SAA
    await demo_rag_enhanced_saa()

if __name__ == "__main__":
    asyncio.run(main())