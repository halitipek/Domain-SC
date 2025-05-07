import os
import sys
import asyncio
import argparse
from pathlib import Path
from typing import List

# Add project root to Python path
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from src.utils.logger import setup_logger
from src.services.rag_service import RagService
from src.services.workflow_service import WorkflowService

# Set up logging
logger = setup_logger(__name__, "setup.log")

async def setup_rag_index(resource_dir: str):
    """Set up RAG index with architectural knowledge resources."""
    logger.info(f"Setting up RAG index with resources from {resource_dir}")
    
    rag_service = RagService()
    
    # Create resources directory if it doesn't exist
    resource_path = Path(resource_dir)
    resource_path.mkdir(exist_ok=True)
    
    # Create sample knowledge files if they don't exist
    create_sample_knowledge_files(resource_path)
    
    # Get all files in the resource directory
    files = [str(f) for f in resource_path.glob("*.md") if f.is_file()]
    
    if not files:
        logger.warning(f"No knowledge files found in {resource_dir}")
        return {"status": "warning", "message": "No knowledge files found"}
    
    # Index the files
    result = rag_service.index_documents(files, collection_name="architecture_knowledge")
    
    return {
        "status": "success", 
        "file_count": len(files),
        "index_result": result
    }

def create_sample_knowledge_files(resource_path: Path):
    """Create sample knowledge files for RAG if they don't exist."""
    # System Architecture knowledge
    create_knowledge_file(
        resource_path / "system_architecture_patterns.md",
        "# System Architecture Patterns\n\n"
        "## Layered Architecture\n\n"
        "A layered architecture organizes the system into horizontal layers, each with a specific role and responsibility.\n\n"
        "## Microservices Architecture\n\n"
        "Microservices architecture structures an application as a collection of loosely coupled services.\n\n"
        "## Event-Driven Architecture\n\n"
        "An event-driven architecture uses events to trigger and communicate between decoupled services."
    )
    
    # API Design knowledge
    create_knowledge_file(
        resource_path / "api_design_best_practices.md",
        "# API Design Best Practices\n\n"
        "## RESTful API Guidelines\n\n"
        "- Use nouns instead of verbs in endpoint paths\n"
        "- Use logical nesting for resources\n"
        "- Use HTTP methods appropriately (GET, POST, PUT, DELETE)\n"
        "- Return appropriate status codes\n\n"
        "## GraphQL Considerations\n\n"
        "- Consider GraphQL for complex data requirements\n"
        "- Implement proper error handling\n"
        "- Optimize resolver performance"
    )
    
    # Module Design knowledge
    create_knowledge_file(
        resource_path / "module_design_principles.md",
        "# Module Design Principles\n\n"
        "## High Cohesion\n\n"
        "Modules should have a single, well-defined responsibility.\n\n"
        "## Loose Coupling\n\n"
        "Minimize dependencies between modules to increase flexibility.\n\n"
        "## Open/Closed Principle\n\n"
        "Modules should be open for extension but closed for modification."
    )
    
    # Requirements Analysis knowledge
    create_knowledge_file(
        resource_path / "requirements_analysis_techniques.md",
        "# Requirements Analysis Techniques\n\n"
        "## User Stories\n\n"
        "As a [user role], I want [goal] so that [benefit].\n\n"
        "## Use Cases\n\n"
        "Detailed scenarios describing interactions between users and the system.\n\n"
        "## Domain Modeling\n\n"
        "Creating a conceptual model of the problem domain, identifying entities and relationships."
    )

def create_knowledge_file(file_path: Path, content: str):
    """Create a knowledge file if it doesn't exist."""
    if not file_path.exists():
        with open(file_path, 'w') as f:
            f.write(content)
        logger.info(f"Created knowledge file: {file_path}")

async def init_sample_workflow():
    """Initialize a sample workflow for testing."""
    logger.info("Initializing sample workflow")
    
    # Create a resources directory for the sample workflow
    sample_dir = Path("./sample")
    sample_dir.mkdir(exist_ok=True)
    
    # Create sample input files
    sample_files = create_sample_input_files(sample_dir)
    
    # Initialize workflow service
    workflow_service = WorkflowService()
    
    # Start the workflow
    result = await workflow_service.initialize_workflow(
        workflow_name="sample_architecture_project",
        input_files=sample_files
    )
    
    # Advance to requirements analysis phase
    await workflow_service.advance_workflow("requirements_analysis")
    
    # Wait a moment to simulate processing
    await asyncio.sleep(1)
    
    # Advance to architecture design phase
    await workflow_service.advance_workflow("architecture_design")
    
    # Send a direct task to the SAA
    await workflow_service.send_direct_task(
        agent_id="SAA",
        task_description="Create the System Architecture Main Plan",
        task_type="create_architecture_document",
        input_data={
            "document_type": "SMAP",
            "input_documents": {"requirements": "Sample requirements content"}
        }
    )
    
    # Get workflow status
    status = workflow_service.get_workflow_status()
    
    return {
        "initialization": result,
        "workflow_status": status
    }

def create_sample_input_files(sample_dir: Path) -> List[str]:
    """Create sample input files for the workflow."""
    # Create a sample requirements document
    req_path = sample_dir / "sample_requirements.md"
    with open(req_path, 'w') as f:
        f.write(
            "# Sample Project Requirements\n\n"
            "## Functional Requirements\n\n"
            "1. The system shall provide document processing capabilities\n"
            "2. The system shall support multiple document formats\n"
            "3. The system shall extract relevant information from documents\n\n"
            "## Non-Functional Requirements\n\n"
            "1. The system shall process documents within 2 seconds\n"
            "2. The system shall be available 99.9% of the time\n"
            "3. The system shall support at least 100 concurrent users"
        )
    
    # Create a sample technology constraints document
    tech_path = sample_dir / "sample_technology.md"
    with open(tech_path, 'w') as f:
        f.write(
            "# Technology Constraints\n\n"
            "## Approved Technologies\n\n"
            "- Python 3.8+\n"
            "- PostgreSQL 13+\n"
            "- Docker\n"
            "- Kubernetes\n\n"
            "## Integration Requirements\n\n"
            "- Must integrate with existing OAuth system\n"
            "- Must support REST APIs\n"
            "- Must support WebSocket for real-time updates"
        )
    
    return [str(req_path), str(tech_path)]

async def main():
    """Main setup function."""
    parser = argparse.ArgumentParser(description="Set up the Domain-SC system")
    parser.add_argument(
        "--setup-rag", action="store_true",
        help="Set up the RAG index with architectural knowledge"
    )
    parser.add_argument(
        "--sample-workflow", action="store_true",
        help="Initialize a sample workflow for testing"
    )
    parser.add_argument(
        "--resource-dir", default="./resources",
        help="Directory for knowledge resources (default: ./resources)"
    )
    
    args = parser.parse_args()
    
    # Create data directory if it doesn't exist
    data_dir = Path("./data")
    data_dir.mkdir(exist_ok=True)
    
    if args.setup_rag:
        result = await setup_rag_index(args.resource_dir)
        print(f"RAG setup result: {result}")
    
    if args.sample_workflow:
        result = await init_sample_workflow()
        print(f"Sample workflow initialized:\n{result}")
    
    if not args.setup_rag and not args.sample_workflow:
        parser.print_help()

if __name__ == "__main__":
    asyncio.run(main())
