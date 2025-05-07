#!/usr/bin/env python
"""
Enhanced Domain-SC System Demonstration

This script demonstrates the integrated capabilities of the Domain-SC system,
including enhanced RAG, optimized LLM service, and simulation-based architecture design.
It performs a complete workflow from initial requirements to architecture generation.
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from typing import Dict, Any, List

# Set up Python path
PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(SRC_PATH))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(PROJECT_ROOT / "logs" / "enhanced_demo.log")
    ]
)
logger = logging.getLogger("enhanced_demo")

# Import key components
from src.services.optimized_llm_service import OptimizedLLMService
from src.services.enhanced_rag_service import EnhancedRAGService
from src.agents.enhanced_system_architect_agent import EnhancedSystemArchitectAgent
from src.prompts.adaptive_prompt_system import AdaptivePromptSystem

class EnhancedSystemDemo:
    """Demonstration of the enhanced Domain-SC system's capabilities."""
    
    def __init__(self):
        """Initialize the demo with all required components."""
        logger.info("Initializing Enhanced Domain-SC Demo")
        
        # Initialize core services
        self.llm_service = OptimizedLLMService()
        self.rag_service = EnhancedRAGService()
        self.prompt_system = AdaptivePromptSystem()
        self.architect_agent = EnhancedSystemArchitectAgent()
        
        # Create output directory if it doesn't exist
        self.output_dir = PROJECT_ROOT / "data" / "output" / "demo_results"
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
        logger.info("Enhanced Domain-SC Demo initialized successfully")
    
    def index_knowledge_resources(self):
        """Index the knowledge resources for RAG."""
        logger.info("Indexing knowledge resources for RAG")
        
        # Get list of resource files
        resource_dir = PROJECT_ROOT / "resources"
        resource_files = list(resource_dir.glob("*.md"))
        resource_paths = [str(path) for path in resource_files]
        
        if not resource_paths:
            logger.warning("No resource files found in resources directory")
            # Create a sample resource file if none exist
            self._create_sample_resource()
            resource_files = list(resource_dir.glob("*.md"))
            resource_paths = [str(path) for path in resource_files]
        
        # Index the documents
        logger.info(f"Indexing {len(resource_paths)} documents")
        self.rag_service.index_documents(resource_paths, collection_name="demo_knowledge")
        logger.info("Knowledge resources indexed successfully")
        
        return resource_paths
    
    def _create_sample_resource(self):
        """Create a sample resource file for demonstration purposes."""
        logger.info("Creating sample resource files")
        
        resource_dir = PROJECT_ROOT / "resources"
        resource_dir.mkdir(exist_ok=True)
        
        # Architecture patterns
        with open(resource_dir / "system_architecture_patterns.md", "w") as f:
            f.write("""# System Architecture Patterns

## Microservices Architecture
Microservices architecture is an architectural style that structures an application as a collection of small, loosely coupled services. Each service is focused on a specific business capability and can be developed, deployed, and scaled independently.

### Key Characteristics
- Service Independence - Each service can be deployed independently
- Domain-Driven Design - Services are organized around business domains
- Decentralized Data Management - Each service manages its own database
- Smart Endpoints, Dumb Pipes - Services communicate through simple protocols
- DevOps Culture - Automated deployment and monitoring

## Event-Driven Architecture
Event-driven architecture is a software design pattern in which decoupled components communicate through events.

### Key Characteristics
- Asynchronous Communication - Components communicate through events
- Loose Coupling - Event producers don't know who consumes events
- Scalability - Easy to add new event consumers
- Resilience - Component failures don't necessarily impact the entire system

## Layered Architecture
Layered architecture organizes the application into horizontal layers, each with a specific responsibility.

### Key Characteristics
- Separation of Concerns - Each layer has a specific responsibility
- Abstraction - Higher layers use the services of lower layers
- Isolation - Changes in one layer shouldn't affect other layers
- Testability - Each layer can be tested independently
""")

        # API design principles
        with open(resource_dir / "api_design_best_practices.md", "w") as f:
            f.write("""# API Design Best Practices

## RESTful API Design
- Use HTTP methods appropriately (GET, POST, PUT, DELETE)
- Use nouns, not verbs, in endpoint paths
- Use plural nouns for collections
- Use nested resources for relationships
- Use proper HTTP status codes
- Implement versioning
- Provide comprehensive documentation

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

        # Module design principles
        with open(resource_dir / "module_design_principles.md", "w") as f:
            f.write("""# Module Design Principles

## High Cohesion
- Keep related code together
- Single responsibility principle
- Minimal external dependencies

## Loose Coupling
- Minimize dependencies between modules
- Use interfaces to hide implementation details
- Dependency inversion principle

## Information Hiding
- Hide implementation details
- Expose minimal interfaces
- Encapsulation of data and behavior

## Open-Closed Principle
- Open for extension, closed for modification
- Use abstraction and polymorphism
- Avoid modifying existing code
""")

        logger.info("Sample resource files created successfully")
    
    def analyze_requirements(self, requirements_text: str) -> Dict[str, Any]:
        """Analyze requirements and extract structured information."""
        logger.info("Analyzing requirements")
        
        prompt = f"""
        Analyze the following requirements and extract key information:
        
        {requirements_text}
        
        Extract and structure the following information:
        1. System purpose and main functionality
        2. Key components needed
        3. Integration requirements
        4. Performance requirements
        5. Security considerations
        6. User types and their needs
        
        Format the result as a detailed JSON structure. Be comprehensive and specific.
        """
        
        result = self.llm_service.generate_text(
            prompt=prompt,
            task_complexity="high"
        )
        
        try:
            # Try to parse as JSON
            structured_requirements = json.loads(result)
            logger.info("Requirements analyzed successfully")
        except json.JSONDecodeError:
            # Fallback if the LLM doesn't return valid JSON
            logger.warning("Failed to parse LLM output as JSON, using text output")
            structured_requirements = {"full_analysis": result}
        
        # Save the structured requirements
        requirements_path = self.output_dir / "structured_requirements.json"
        with open(requirements_path, "w") as f:
            json.dump(structured_requirements, f, indent=2)
        
        return structured_requirements
    
    def enhance_with_rag(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance the requirements with information from the RAG system."""
        logger.info("Enhancing requirements with RAG")
        
        # Create a query for the RAG system
        if "system_purpose" in requirements:
            query = f"Architecture patterns for {requirements['system_purpose']}"
        else:
            query = "Recommend architecture patterns for a modern application"
        
        # Retrieve relevant documents
        retrieved_docs = self.rag_service.semantic_retrieval(query, min_relevance=0.4)
        logger.info(f"Retrieved {len(retrieved_docs)} relevant documents")
        
        # Extract and save the relevant information
        retrieved_content = []
        for doc in retrieved_docs:
            content = doc.get("text", "") or doc.get("document", "")
            source = doc.get("source", "Unknown")
            retrieved_content.append({
                "source": source,
                "content": content[:500] + "..." if len(content) > 500 else content,
                "relevance": doc.get("relevance", 0)
            })
        
        # Save the RAG results
        rag_path = self.output_dir / "rag_results.json"
        with open(rag_path, "w") as f:
            json.dump(retrieved_content, f, indent=2)
        
        # Return the enhanced requirements
        return {
            **requirements,
            "rag_enhancements": retrieved_content
        }
    
    def convert_to_design_input(self, enhanced_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Convert the enhanced requirements to a format suitable for the architecture design."""
        logger.info("Preparing design input from enhanced requirements")
        
        # Extract main requirements
        if "system_purpose" in enhanced_requirements:
            description = enhanced_requirements["system_purpose"]
        else:
            # Extract from full analysis if structured format is not available
            description = "System based on analyzed requirements"
        
        # Extract features
        features = []
        if "key_components" in enhanced_requirements:
            if isinstance(enhanced_requirements["key_components"], list):
                features = enhanced_requirements["key_components"]
            else:
                features = [enhanced_requirements["key_components"]]
        
        # Extract performance requirements
        performance = ""
        if "performance_requirements" in enhanced_requirements:
            if isinstance(enhanced_requirements["performance_requirements"], str):
                performance = enhanced_requirements["performance_requirements"]
            elif isinstance(enhanced_requirements["performance_requirements"], dict):
                performance = json.dumps(enhanced_requirements["performance_requirements"])
            elif isinstance(enhanced_requirements["performance_requirements"], list):
                performance = ", ".join(enhanced_requirements["performance_requirements"])
        
        # Build constraints
        constraints = {}
        if "security_considerations" in enhanced_requirements:
            constraints["security"] = enhanced_requirements["security_considerations"]
        if "integration_requirements" in enhanced_requirements:
            constraints["integration"] = enhanced_requirements["integration_requirements"]
        
        # Add RAG-derived technology suggestions if available
        if "rag_enhancements" in enhanced_requirements and enhanced_requirements["rag_enhancements"]:
            # Prepare a prompt to extract technology recommendations from RAG results
            rag_content = "\n".join([item.get("content", "") for item in enhanced_requirements["rag_enhancements"]])
            tech_prompt = f"""
            Based on the following retrieved information, suggest appropriate technologies and architectural patterns:
            
            {rag_content}
            
            Provide a concise list of recommended technologies and patterns.
            """
            
            tech_suggestions = self.llm_service.generate_text(prompt=tech_prompt, task_complexity="medium")
            constraints["technology_suggestions"] = tech_suggestions
        
        # Create the final design input structure
        design_input = {
            "requirements": {
                "description": description,
                "features": features,
                "performance": performance,
                "scale": "Medium (500 concurrent users)"  # Default value
            },
            "constraints": constraints
        }
        
        # Save the design input
        design_input_path = self.output_dir / "design_input.json"
        with open(design_input_path, "w") as f:
            json.dump(design_input, f, indent=2)
        
        logger.info("Design input prepared successfully")
        return design_input
    
    def generate_architecture(self, design_input: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the system architecture using the enhanced architect agent."""
        logger.info("Generating system architecture")
        
        requirements = design_input["requirements"]
        constraints = design_input["constraints"]
        
        # Start the architecture design process
        start_time = time.time()
        architecture = self.architect_agent.design_architecture(requirements, constraints)
        end_time = time.time()
        
        logger.info(f"Architecture design completed in {end_time - start_time:.2f} seconds")
        
        # Save the generated architecture
        architecture_path = self.output_dir / "generated_architecture.json"
        with open(architecture_path, "w") as f:
            json.dump(architecture, f, indent=2)
        
        # Also save a markdown version for better readability
        self._save_architecture_markdown(architecture)
        
        return architecture
    
    def _save_architecture_markdown(self, architecture: Dict[str, Any]):
        """Save the architecture in a readable markdown format."""
        md_content = "# Generated System Architecture\n\n"
        
        # Add overview
        if "overview" in architecture:
            md_content += "## Overview\n\n"
            md_content += f"{architecture['overview']}\n\n"
        
        # Add components
        if "components" in architecture:
            md_content += "## Components\n\n"
            for i, component in enumerate(architecture["components"], 1):
                md_content += f"### {i}. {component.get('name', f'Component {i}')}\n\n"
                md_content += f"{component.get('description', 'No description')}\n\n"
                
                # Add responsibilities
                if "responsibilities" in component:
                    md_content += "**Responsibilities:**\n\n"
                    for resp in component["responsibilities"]:
                        md_content += f"- {resp}\n"
                    md_content += "\n"
                
                # Add interfaces
                if "interfaces" in component:
                    md_content += "**Interfaces:**\n\n"
                    for intf in component["interfaces"]:
                        md_content += f"- {intf}\n"
                    md_content += "\n"
        
        # Add data flows
        if "data_flows" in architecture:
            md_content += "## Data Flows\n\n"
            for i, flow in enumerate(architecture["data_flows"], 1):
                md_content += f"{i}. {flow.get('source', 'Source')} → {flow.get('destination', 'Destination')}: {flow.get('description', 'No description')}\n"
            md_content += "\n"
        
        # Add deployment strategy
        if "deployment" in architecture:
            md_content += "## Deployment Strategy\n\n"
            md_content += f"{architecture['deployment']}\n\n"
        
        # Add recommendations
        if "recommendations" in architecture:
            md_content += "## Recommendations\n\n"
            for i, rec in enumerate(architecture["recommendations"], 1):
                md_content += f"{i}. {rec}\n"
            md_content += "\n"
        
        # Save the markdown file
        md_path = self.output_dir / "generated_architecture.md"
        with open(md_path, "w") as f:
            f.write(md_content)
        
        logger.info(f"Architecture saved as markdown at {md_path}")
    
    def run_complete_workflow(self, requirements_text: str):
        """Run the complete workflow from requirements to architecture."""
        logger.info("Starting complete workflow")
        
        # Step 1: Index knowledge resources for RAG
        self.index_knowledge_resources()
        
        # Step 2: Analyze the requirements
        structured_requirements = self.analyze_requirements(requirements_text)
        
        # Step 3: Enhance with RAG
        enhanced_requirements = self.enhance_with_rag(structured_requirements)
        
        # Step 4: Convert to design input
        design_input = self.convert_to_design_input(enhanced_requirements)
        
        # Step 5: Generate architecture
        architecture = self.generate_architecture(design_input)
        
        logger.info("Complete workflow completed successfully")
        
        # Return paths to the generated artifacts
        return {
            "requirements": str(self.output_dir / "structured_requirements.json"),
            "rag_results": str(self.output_dir / "rag_results.json"),
            "design_input": str(self.output_dir / "design_input.json"),
            "architecture_json": str(self.output_dir / "generated_architecture.json"),
            "architecture_md": str(self.output_dir / "generated_architecture.md")
        }


def main():
    """Main function to run the demo."""
    # Sample requirements text
    sample_requirements = """
    We need to build a modern e-commerce platform that can handle high traffic volumes 
    and scale during peak shopping seasons like Black Friday. The system should provide
    a personalized shopping experience, integrate with multiple payment providers, and
    offer real-time inventory management.
    
    The platform should have a mobile app and web interface for customers, an admin
    dashboard for store managers, and integration capabilities with external logistics
    providers for shipping.
    
    Key features include:
    - Product catalog with categories, search, and filtering
    - User accounts with order history and saved preferences
    - Shopping cart and checkout process
    - Payment processing with multiple providers
    - Order management and tracking
    - Inventory management with alerts for low stock
    - Analytics dashboard for business insights
    - Marketing tools for promotions and discounts
    
    Performance requirements:
    - Support for at least 10,000 concurrent users
    - Page load times under 2 seconds
    - 99.9% uptime
    
    Security considerations:
    - PCI DSS compliance for payment processing
    - GDPR compliance for user data
    - Protection against common vulnerabilities (XSS, CSRF, etc.)
    """
    
    # Create and run the demo
    demo = EnhancedSystemDemo()
    result_paths = demo.run_complete_workflow(sample_requirements)
    
    # Print the paths to the generated artifacts
    print("\n=== Enhanced Domain-SC Demo Results ===\n")
    for key, path in result_paths.items():
        print(f"{key}: {path}")
    print("\nDemo completed successfully. Check the output files for detailed results.")


if __name__ == "__main__":
    main()