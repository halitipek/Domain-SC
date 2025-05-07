"""
Demo-related commands for the Domain-SC CLI.
"""

import argparse
import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.services.enhanced_rag_service import EnhancedRAGService
from src.services.workflow_service import WorkflowService
from src.utils.logger import setup_logger

# Set up logging
logger = setup_logger("cli.demo")


def register_commands(subparsers: argparse._SubParsersAction) -> None:
    """
    Register demo-related commands.
    
    Args:
        subparsers: Subparser group to add to
    """
    # Demo command group
    demo_parser = subparsers.add_parser("demo", help="Demo-related commands")
    demo_subparsers = demo_parser.add_subparsers(dest="demo_command", help="Demo command to execute")
    
    # Demo setup command
    demo_setup_parser = demo_subparsers.add_parser("setup", help="Set up the demo environment")
    demo_setup_parser.add_argument("--resources-dir", help="Directory for demo resources")
    demo_setup_parser.add_argument("--sample-dir", help="Directory for sample files")
    
    # Demo workflow command
    demo_workflow_parser = demo_subparsers.add_parser("workflow", help="Run a sample workflow")
    demo_workflow_parser.add_argument("--output-dir", "-o", help="Output directory for results")
    
    # Demo quickstart command
    demo_quickstart_parser = demo_subparsers.add_parser("quickstart", help="Run a quick demo with simplified output")
    demo_quickstart_parser.add_argument("--requirements", "-r", help="Custom requirements text (uses default if not provided)")
    
    # Demo enhanced command
    demo_enhanced_parser = demo_subparsers.add_parser("enhanced", help="Run enhanced system demo")
    demo_enhanced_parser.add_argument("--input-file", "-i", help="Input requirements file")
    demo_enhanced_parser.add_argument("--output-dir", "-o", help="Output directory for results")


def print_json(data: Any) -> None:
    """
    Print data as formatted JSON.
    
    Args:
        data: Data to print
    """
    print(json.dumps(data, indent=2))


async def handle_commands(args: argparse.Namespace, config: Any) -> int:
    """
    Handle demo-related commands.
    
    Args:
        args: Parsed command line arguments
        config: CLI configuration
        
    Returns:
        int: Exit code (0 for success, non-zero for error)
    """
    # Get root directory
    root_dir = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
    
    if args.demo_command == "setup":
        # Initialize services
        rag_service = EnhancedRAGService()
        
        # Get directories
        resources_dir = Path(args.resources_dir) if args.resources_dir else root_dir / "resources"
        sample_dir = Path(args.sample_dir) if args.sample_dir else root_dir / "data" / "test_cases" / "example_case"
        
        # Create directories if they don't exist
        resources_dir.mkdir(exist_ok=True, parents=True)
        sample_dir.mkdir(exist_ok=True, parents=True)
        
        # Create sample files
        print("Creating sample files...")
        
        # Sample requirements document
        req_path = sample_dir / "requirements.md"
        with open(req_path, 'w') as f:
            f.write(
                "# Sample Project Requirements\n\n"
                "## Functional Requirements\n\n"
                "1. The system shall provide document processing capabilities\n"
                "2. The system shall support multiple document formats (PDF, DOCX, TXT)\n"
                "3. The system shall extract relevant information from documents using NLP\n"
                "4. The system shall provide a search interface for document contents\n"
                "5. The system shall allow users to categorize and tag documents\n\n"
                "## Non-Functional Requirements\n\n"
                "1. The system shall process documents within 2 seconds for files under 5MB\n"
                "2. The system shall be available 99.9% of the time\n"
                "3. The system shall support at least 100 concurrent users\n"
                "4. The system shall implement role-based access control\n"
                "5. The system shall encrypt all stored documents"
            )
        
        # Sample technology constraints document
        tech_path = sample_dir / "technology_constraints.md"
        with open(tech_path, 'w') as f:
            f.write(
                "# Technology Constraints\n\n"
                "## Approved Technologies\n\n"
                "- Frontend: React with TypeScript\n"
                "- Backend: Python 3.8+ with FastAPI\n"
                "- Database: PostgreSQL 13+\n"
                "- Search: Elasticsearch\n"
                "- Infrastructure: Docker, Kubernetes\n"
                "- CI/CD: GitHub Actions\n\n"
                "## Integration Requirements\n\n"
                "- Must integrate with existing OAuth2 authentication system\n"
                "- Must support REST APIs with OpenAPI documentation\n"
                "- Must support WebSocket for real-time notifications\n"
                "- Must provide SDK for Java and Python clients\n\n"
                "## Compliance Requirements\n\n"
                "- GDPR compliance for all user data\n"
                "- SOC 2 compliance for security controls\n"
                "- ADA compliance for accessibility"
            )
            
        # Sample optimization goals document
        opt_path = sample_dir / "optimization_goals.md"
        with open(opt_path, 'w') as f:
            f.write(
                "# Optimization Goals\n\n"
                "## Performance Goals\n\n"
                "- Document processing time < 2 seconds for 5MB files\n"
                "- Search response time < 200ms\n"
                "- API response time < 100ms for 95% of requests\n\n"
                "## Scalability Goals\n\n"
                "- Support for 1000+ concurrent users\n"
                "- Ability to process 100,000+ documents daily\n"
                "- Horizontal scaling for all components\n\n"
                "## Cost Optimization\n\n"
                "- Minimize cloud infrastructure costs\n"
                "- Implement tiered storage for less frequently accessed documents\n"
                "- Optimize search index size and performance"
            )
        
        # Sample architecture knowledge files
        print("Creating sample knowledge files...")
        
        # Architecture patterns
        arch_path = resources_dir / "architecture_patterns.md"
        with open(arch_path, 'w') as f:
            f.write(
                "# Architecture Patterns\n\n"
                "## Microservices Architecture\n\n"
                "Microservices architecture is a style that structures an application as a collection of loosely coupled services. Each service is focused on a specific business capability and can be developed, deployed, and scaled independently.\n\n"
                "### Key Characteristics\n\n"
                "- Services are organized around business capabilities\n"
                "- Services are independently deployable\n"
                "- Services are loosely coupled\n"
                "- Services communicate via APIs\n"
                "- Each service has its own database\n\n"
                "## Event-Driven Architecture\n\n"
                "An event-driven architecture uses events to trigger and communicate between decoupled services. It enables loose coupling and high scalability.\n\n"
                "### Key Characteristics\n\n"
                "- Events represent state changes in the system\n"
                "- Services publish events to event channels\n"
                "- Services subscribe to events they are interested in\n"
                "- Asynchronous communication model\n"
                "- Good for real-time systems and high-throughput scenarios\n\n"
                "## Layered Architecture\n\n"
                "Layered architecture organizes the system into horizontal layers, each with a specific role and responsibility. Common layers include presentation, business logic, and data access.\n\n"
                "### Key Characteristics\n\n"
                "- Separation of concerns between layers\n"
                "- Each layer has a specific responsibility\n"
                "- Upper layers depend on lower layers\n"
                "- Changes to one layer should not affect other layers\n"
                "- Good for simple applications with clear separations"
            )
        
        # API design
        api_path = resources_dir / "api_design_patterns.md"
        with open(api_path, 'w') as f:
            f.write(
                "# API Design Patterns\n\n"
                "## RESTful API Design\n\n"
                "### Best Practices\n\n"
                "- Use nouns instead of verbs in endpoint paths\n"
                "- Use logical nesting for resources\n"
                "- Use HTTP methods appropriately (GET, POST, PUT, DELETE)\n"
                "- Return appropriate status codes\n"
                "- Use pagination for large result sets\n"
                "- Implement proper error handling\n"
                "- Version your APIs\n"
                "- Use HATEOAS for discoverability\n\n"
                "## GraphQL API Design\n\n"
                "### Best Practices\n\n"
                "- Define a clear schema\n"
                "- Use appropriate types (scalar, object, input, etc.)\n"
                "- Implement proper error handling\n"
                "- Optimize resolver performance\n"
                "- Use pagination for large result sets\n"
                "- Consider batching and caching\n"
                "- Implement proper authentication and authorization\n\n"
                "## API Gateway Pattern\n\n"
                "### Key Features\n\n"
                "- Single entry point for all clients\n"
                "- API composition\n"
                "- Protocol translation\n"
                "- Rate limiting and throttling\n"
                "- Authentication and authorization\n"
                "- Monitoring and analytics\n"
                "- Circuit breaking for fault tolerance"
            )
        
        # Database design
        db_path = resources_dir / "database_design_patterns.md"
        with open(db_path, 'w') as f:
            f.write(
                "# Database Design Patterns\n\n"
                "## Relational Database Design\n\n"
                "### Best Practices\n\n"
                "- Normalize data to reduce redundancy\n"
                "- Use appropriate indexes for performance\n"
                "- Implement proper constraints for data integrity\n"
                "- Design for query optimization\n"
                "- Use appropriate data types\n"
                "- Implement proper access controls\n\n"
                "## NoSQL Database Design\n\n"
                "### Document Databases\n\n"
                "- Design for document access patterns\n"
                "- Denormalize data for read optimization\n"
                "- Use appropriate indexes\n"
                "- Consider document size limitations\n\n"
                "### Key-Value Stores\n\n"
                "- Design keys for efficient access\n"
                "- Consider data eviction policies\n"
                "- Use for simple, high-throughput operations\n\n"
                "## Database Scaling Patterns\n\n"
                "### Horizontal Scaling\n\n"
                "- Sharding strategies\n"
                "- Replication patterns\n"
                "- Read replicas vs. write replicas\n\n"
                "### Caching Strategies\n\n"
                "- Cache-aside pattern\n"
                "- Write-through cache\n"
                "- Write-behind cache\n"
                "- Refresh-ahead cache"
            )
        
        # Index the knowledge files
        print("Indexing knowledge files...")
        knowledge_files = [str(arch_path), str(api_path), str(db_path)]
        result = await rag_service.index_documents(
            file_paths=knowledge_files,
            collection_name="demo_knowledge"
        )
        
        print("Demo setup completed successfully!")
        print(f"Sample files created in: {sample_dir}")
        print(f"Knowledge resources created in: {resources_dir}")
        print(f"Indexed {len(knowledge_files)} knowledge files: {result.get('indexed_count', 0)} chunks created")
        
        return 0
        
    elif args.demo_command == "workflow":
        # Initialize services
        workflow_service = WorkflowService()
        
        # Get sample directory
        sample_dir = root_dir / "data" / "test_cases" / "example_case"
        if not sample_dir.exists():
            print(f"Error: Sample directory not found: {sample_dir}")
            print("Run 'domain-sc demo setup' first to create sample files.")
            return 1
        
        # Check if sample files exist
        req_path = sample_dir / "requirements.md"
        tech_path = sample_dir / "technology_constraints.md"
        opt_path = sample_dir / "optimization_goals.md"
        
        if not req_path.exists() or not tech_path.exists() or not opt_path.exists():
            print("Error: Sample files not found.")
            print("Run 'domain-sc demo setup' first to create sample files.")
            return 1
        
        # Get output directory
        output_dir = args.output_dir or config.get("workflow", "output_path")
        os.makedirs(output_dir, exist_ok=True)
        
        # Create workflow
        print("Creating workflow...")
        workflow_result = await workflow_service.initialize_workflow(
            name="demo_workflow",
            input_files=[str(req_path), str(tech_path), str(opt_path)],
            output_dir=output_dir
        )
        
        workflow_id = workflow_result.get("workflow_id")
        if not workflow_id:
            print("Error: Failed to create workflow.")
            return 1
            
        print(f"Workflow created with ID: {workflow_id}")
        
        # Advance to requirements analysis phase
        print("Advancing to requirements analysis phase...")
        await workflow_service.advance_workflow(workflow_id, "requirements_analysis")
        
        # Send a task to the Requirements Analysis Agent
        print("Sending task to Requirements Analysis Agent...")
        await workflow_service.send_direct_task(
            workflow_id=workflow_id,
            agent_id="RAA",
            task_description="Analyze requirements from the sample documents",
            task_type="analyze_requirements",
            input_data={
                "documents": {
                    "requirements.md": open(req_path).read()
                }
            }
        )
        
        # Wait a moment to simulate processing
        print("Processing requirements...")
        time.sleep(2)
        
        # Advance to technology analysis phase
        print("Advancing to technology analysis phase...")
        await workflow_service.advance_workflow(workflow_id, "technology_analysis")
        
        # Send a task to the Technology Analysis Agent
        print("Sending task to Technology Analysis Agent...")
        await workflow_service.send_direct_task(
            workflow_id=workflow_id,
            agent_id="TAA",
            task_description="Analyze technology requirements from the sample documents",
            task_type="analyze_technology",
            input_data={
                "documents": {
                    "technology_constraints.md": open(tech_path).read(),
                    "optimization_goals.md": open(opt_path).read()
                }
            }
        )
        
        # Wait a moment to simulate processing
        print("Processing technology constraints...")
        time.sleep(2)
        
        # Advance to architecture design phase
        print("Advancing to architecture design phase...")
        await workflow_service.advance_workflow(workflow_id, "architecture_design")
        
        # Send a task to the System Architect Agent
        print("Sending task to System Architect Agent...")
        await workflow_service.send_direct_task(
            workflow_id=workflow_id,
            agent_id="SAA",
            task_description="Create the System Architecture Design Document",
            task_type="create_architecture_document",
            input_data={
                "document_type": "SADD",
                "input_documents": {
                    "requirements": open(req_path).read(),
                    "technology": open(tech_path).read(),
                    "optimization": open(opt_path).read()
                }
            }
        )
        
        # Wait a moment to simulate processing
        print("Generating architecture design...")
        time.sleep(3)
        
        # Finalize workflow
        print("Finalizing workflow...")
        result = await workflow_service.finalize_workflow(workflow_id)
        
        # Get workflow status
        print("Getting workflow status...")
        status = await workflow_service.get_workflow_status(workflow_id)
        
        # Export results
        export_dir = Path(output_dir) / f"demo_workflow_{workflow_id}"
        export_dir.mkdir(exist_ok=True, parents=True)
        
        await workflow_service.export_workflow_results(
            workflow_id=workflow_id,
            output_dir=str(export_dir),
            format="all"
        )
        
        print(f"\nDemo workflow completed successfully!")
        print(f"Results exported to: {export_dir}")
        
        return 0
        
    elif args.demo_command == "quickstart":
        # Import demo module to run quickstart
        from demo_enhanced_system import EnhancedSystemDemo
        
        # Get custom requirements or use default
        if args.requirements:
            requirements_text = args.requirements
        else:
            requirements_text = (
                "Create a document management system that can process multiple document formats, "
                "extract text with OCR, support search with natural language queries, "
                "and provide a REST API for integration. The system should be scalable, "
                "secure, and have high availability."
            )
        
        # Create and run demo
        print("Running quickstart demo...")
        print(f"Requirements: {requirements_text}")
        
        demo = EnhancedSystemDemo()
        result = await demo.run_quick_demo(requirements_text)
        
        print("\nQuickstart demo completed successfully!")
        print("\nArchitecture Overview:")
        print(result.get("architecture_overview", "Architecture overview not available"))
        
        return 0
        
    elif args.demo_command == "enhanced":
        # Import demo module
        from demo_enhanced_system import EnhancedSystemDemo
        
        # Get input file if specified
        if args.input_file:
            if not os.path.exists(args.input_file):
                print(f"Error: Input file not found: {args.input_file}")
                return 1
                
            with open(args.input_file, 'r') as f:
                requirements_text = f.read()
        else:
            # Use default requirements
            requirements_text = (
                "# Document Management System Requirements\n\n"
                "## Functional Requirements\n\n"
                "1. The system shall process multiple document formats (PDF, DOCX, images)\n"
                "2. The system shall extract text with OCR from scanned documents\n"
                "3. The system shall support full-text search with natural language queries\n"
                "4. The system shall classify documents automatically based on content\n"
                "5. The system shall provide version control for documents\n"
                "6. The system shall support document annotation and collaboration\n"
                "7. The system shall provide a REST API for integration\n\n"
                "## Non-Functional Requirements\n\n"
                "1. The system shall handle processing of 1000+ documents per day\n"
                "2. The system shall achieve 99.9% uptime\n"
                "3. The system shall provide role-based access control\n"
                "4. The system shall encrypt all stored documents\n"
                "5. The system shall comply with GDPR and SOC 2 requirements\n"
            )
        
        # Get output directory
        output_dir = Path(args.output_dir) if args.output_dir else Path(config.get("workflow", "output_path")) / "enhanced_demo"
        output_dir.mkdir(exist_ok=True, parents=True)
        
        # Create and run demo
        print("Running enhanced system demo...")
        print(f"Output directory: {output_dir}")
        
        demo = EnhancedSystemDemo()
        await demo.run_complete_workflow(requirements_text, output_dir=str(output_dir))
        
        print("\nEnhanced demo completed successfully!")
        print(f"Results saved to: {output_dir}")
        
        return 0
    
    else:
        print("Unknown demo command. Use 'domain-sc demo --help' for available commands.")
        return 1