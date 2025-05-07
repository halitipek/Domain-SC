#!/usr/bin/env python
"""
Command-line interface for the Domain-SC system.
This script provides a convenient way to interact with the system from the command line.
"""

import os
import sys
import json
import argparse
import asyncio
from pathlib import Path
import time
from typing import List, Dict, Any, Optional

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parent
sys.path.append(str(ROOT_DIR))

from src.services.rag_service import RagService
from src.services.workflow_service import WorkflowService
from src.services.llm_service import LLMService
from src.prompts.prompt_manager import PromptManager

# Create global service instances
rag_service = None
workflow_service = None
llm_service = None
prompt_manager = None

def init_services():
    """Initialize service instances."""
    global rag_service, workflow_service, llm_service, prompt_manager
    
    if rag_service is None:
        print("Initializing services...")
        rag_service = RagService()
        workflow_service = WorkflowService()
        llm_service = LLMService()
        prompt_manager = PromptManager()
        print("Services initialized.")

def print_json(data):
    """Print data as formatted JSON."""
    print(json.dumps(data, indent=2))

async def handle_rag_commands(args):
    """Handle RAG-related commands."""
    init_services()
    
    if args.rag_command == 'index':
        # Index documents
        if not args.files:
            print("Error: Please provide at least one file path to index.")
            return
        
        result = rag_service.index_documents(args.files, args.collection)
        print_json(result)
        
    elif args.rag_command == 'query':
        # Query the RAG system
        if not args.query:
            print("Error: Please provide a query.")
            return
        
        result = rag_service.query(args.query, args.agent_type, args.top_k)
        print_json(result)
        
    elif args.rag_command == 'stats':
        # Get RAG statistics
        stats = rag_service.get_stats()
        print_json(stats)
        
    elif args.rag_command == 'clear':
        # Clear the RAG index
        rag_service.clear_index()
        print("RAG index cleared successfully.")

async def handle_workflow_commands(args):
    """Handle workflow-related commands."""
    init_services()
    
    if args.workflow_command == 'create':
        # Create a new workflow
        if not args.name:
            print("Error: Please provide a workflow name.")
            return
        
        if not args.files:
            print("Error: Please provide at least one input file.")
            return
        
        result = await workflow_service.initialize_workflow(args.name, args.files)
        print_json(result)
        
    elif args.workflow_command == 'list':
        # List all workflows
        result = workflow_service.get_workflow_status()
        print_json(result)
        
    elif args.workflow_command == 'status':
        # Get workflow status
        if not args.workflow_id:
            print("Error: Please provide a workflow ID.")
            return
        
        result = workflow_service.get_workflow_status(args.workflow_id)
        if "status" in result and result["status"] == "error":
            print(f"Error: {result['message']}")
            return
            
        print_json(result)
        
    elif args.workflow_command == 'advance':
        # Advance workflow to next phase
        if not args.workflow_id:
            print("Error: Please provide a workflow ID.")
            return
            
        if not args.phase:
            print("Error: Please provide a phase name.")
            return
        
        result = await workflow_service.advance_workflow(args.workflow_id, args.phase)
        if "status" in result and result["status"] == "error":
            print(f"Error: {result['message']}")
            return
            
        print_json(result)
        
    elif args.workflow_command == 'task':
        # Send a task to an agent
        if not args.workflow_id or not args.agent_id or not args.task_type or not args.description:
            print("Error: Please provide workflow ID, agent ID, task type, and description.")
            return
        
        # Parse input data JSON if provided
        input_data = {}
        if args.input_data:
            try:
                input_data = json.loads(args.input_data)
            except json.JSONDecodeError:
                print("Error: Invalid JSON format for input data.")
                return
        
        result = await workflow_service.send_direct_task(
            args.workflow_id,
            args.agent_id,
            args.description,
            args.task_type,
            input_data
        )
        
        if "status" in result and result["status"] == "error":
            print(f"Error: {result['message']}")
            return
            
        print_json(result)
        
    elif args.workflow_command == 'finalize':
        # Finalize workflow
        if not args.workflow_id:
            print("Error: Please provide a workflow ID.")
            return
        
        result = await workflow_service.finalize_workflow(args.workflow_id)
        if "status" in result and result["status"] == "error":
            print(f"Error: {result['message']}")
            return
            
        print_json(result)

async def handle_llm_commands(args):
    """Handle LLM-related commands."""
    init_services()
    
    if args.llm_command == 'generate':
        # Generate text using the LLM
        if not args.prompt:
            # If prompt not provided as argument, read from stdin
            print("Enter prompt (Ctrl+D to finish):")
            prompt_lines = []
            try:
                while True:
                    line = input()
                    prompt_lines.append(line)
            except EOFError:
                prompt = "\n".join(prompt_lines)
        else:
            prompt = args.prompt
        
        if not prompt.strip():
            print("Error: Empty prompt.")
            return
        
        print("Generating response...")
        response = llm_service.generate_text(
            prompt=prompt,
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens
        )
        
        print("\n----- Generated Response -----\n")
        print(response)
        print("\n-----------------------------\n")
        
    elif args.llm_command == 'agent-prompt':
        # Generate text using an agent's prompt template
        if not args.agent_id or not args.prompt_type:
            print("Error: Please provide agent ID and prompt type.")
            return
        
        # Parse variables JSON if provided
        variables = {}
        if args.variables:
            try:
                variables = json.loads(args.variables)
            except json.JSONDecodeError:
                print("Error: Invalid JSON format for variables.")
                return
        
        print("Generating response with agent prompt...")
        response = llm_service.generate_with_agent_prompt(
            agent_id=args.agent_id,
            prompt_type=args.prompt_type,
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            **variables
        )
        
        print("\n----- Generated Response -----\n")
        print(response)
        print("\n-----------------------------\n")
        
    elif args.llm_command == 'templates':
        # List available prompt templates
        if args.agent_id:
            # Get templates for specific agent
            template = prompt_manager.get_template(args.agent_id)
            if not template:
                print(f"No templates found for agent {args.agent_id}")
                return
                
            print_json({"agent_id": args.agent_id, "templates": template})
        else:
            # Get all templates
            templates = {}
            for agent_id in prompt_manager.templates:
                templates[agent_id] = list(prompt_manager.templates[agent_id].keys())
            
            print_json({"templates": templates})

async def handle_demo_commands(args):
    """Handle demo-related commands."""
    init_services()
    
    if args.demo_command == 'setup':
        # Run setup tasks for the demo
        print("Setting up demo environment...")
        
        # Create resources directory if it doesn't exist
        resources_dir = ROOT_DIR / "resources"
        resources_dir.mkdir(exist_ok=True)
        
        # Create sample directory if it doesn't exist
        sample_dir = ROOT_DIR / "sample"
        sample_dir.mkdir(exist_ok=True)
        
        # Create sample files
        print("Creating sample files...")
        
        # Sample requirements document
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
        
        # Sample technology document
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
        
        # Sample architecture knowledge files
        print("Creating sample knowledge files...")
        
        # Architecture patterns
        arch_path = resources_dir / "architecture_patterns.md"
        with open(arch_path, 'w') as f:
            f.write(
                "# Architecture Patterns\n\n"
                "## Microservices Architecture\n\n"
                "Microservices architecture is a style that structures an application as a collection of loosely coupled services. Each service is focused on a specific business capability and can be developed, deployed, and scaled independently.\n\n"
                "## Layered Architecture\n\n"
                "Layered architecture organizes the system into horizontal layers, each with a specific role and responsibility. Common layers include presentation, business logic, and data access.\n\n"
                "## Event-Driven Architecture\n\n"
                "An event-driven architecture uses events to trigger and communicate between decoupled services. It enables loose coupling and high scalability."
            )
        
        # API design
        api_path = resources_dir / "api_design.md"
        with open(api_path, 'w') as f:
            f.write(
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
        
        # Index the knowledge files
        print("Indexing knowledge files...")
        knowledge_files = [str(arch_path), str(api_path)]
        rag_service.index_documents(knowledge_files, "demo_knowledge")
        
        print("Demo setup completed successfully!")
        
    elif args.demo_command == 'workflow':
        # Run a sample workflow
        print("Starting sample workflow...")
        
        # Check if sample files exist
        sample_dir = ROOT_DIR / "sample"
        if not sample_dir.exists():
            print("Error: Sample directory not found. Run 'demo setup' first.")
            return
        
        req_path = sample_dir / "sample_requirements.md"
        tech_path = sample_dir / "sample_technology.md"
        
        if not req_path.exists() or not tech_path.exists():
            print("Error: Sample files not found. Run 'demo setup' first.")
            return
        
        # Create workflow
        print("Creating workflow...")
        workflow_result = await workflow_service.initialize_workflow(
            "demo_workflow",
            [str(req_path), str(tech_path)]
        )
        
        workflow_id = workflow_result["workflow_id"]
        print(f"Workflow created with ID: {workflow_id}")
        
        # Advance to requirements analysis phase
        print("Advancing to requirements analysis phase...")
        await workflow_service.advance_workflow(workflow_id, "requirements_analysis")
        
        # Send a task to the RAA
        print("Sending task to Requirements Analysis Agent...")
        await workflow_service.send_direct_task(
            workflow_id=workflow_id,
            agent_id="RAA",
            task_description="Analyze requirements from the sample documents",
            task_type="analyze_requirements",
            input_data={"documents": {"sample_requirements.md": open(req_path).read()}}
        )
        
        # Wait a moment to simulate processing
        print("Processing...")
        time.sleep(2)
        
        # Advance to technology analysis phase
        print("Advancing to technology analysis phase...")
        await workflow_service.advance_workflow(workflow_id, "technology_analysis")
        
        # Send a task to the TAA
        print("Sending task to Technology Analysis Agent...")
        await workflow_service.send_direct_task(
            workflow_id=workflow_id,
            agent_id="TAA",
            task_description="Analyze technology requirements from the sample documents",
            task_type="analyze_technology",
            input_data={"documents": {"sample_technology.md": open(tech_path).read()}}
        )
        
        # Wait a moment to simulate processing
        print("Processing...")
        time.sleep(2)
        
        # Advance to architecture design phase
        print("Advancing to architecture design phase...")
        await workflow_service.advance_workflow(workflow_id, "architecture_design")
        
        # Send a task to the SAA
        print("Sending task to System Architect Agent...")
        await workflow_service.send_direct_task(
            workflow_id=workflow_id,
            agent_id="SAA",
            task_description="Create the System Architecture Main Plan",
            task_type="create_architecture_document",
            input_data={
                "document_type": "SMAP",
                "input_documents": {
                    "requirements": open(req_path).read(),
                    "technology": open(tech_path).read()
                }
            }
        )
        
        # Wait a moment to simulate processing
        print("Processing...")
        time.sleep(2)
        
        # Get workflow status
        print("Getting workflow status...")
        status = workflow_service.get_workflow_status(workflow_id)
        print_json(status)
        
        print("\nDemo workflow completed successfully!")

def setup_parser():
    """Set up the argument parser."""
    parser = argparse.ArgumentParser(description="Domain-SC Command Line Interface")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # RAG commands
    rag_parser = subparsers.add_parser("rag", help="RAG-related commands")
    rag_subparsers = rag_parser.add_subparsers(dest="rag_command", help="RAG command to execute")
    
    # RAG index command
    rag_index_parser = rag_subparsers.add_parser("index", help="Index documents for RAG")
    rag_index_parser.add_argument("--files", "-f", nargs="+", help="Files to index")
    rag_index_parser.add_argument("--collection", "-c", help="Collection name")
    
    # RAG query command
    rag_query_parser = rag_subparsers.add_parser("query", help="Query the RAG system")
    rag_query_parser.add_argument("--query", "-q", help="Query string")
    rag_query_parser.add_argument("--agent-type", "-a", help="Agent type to get context for")
    rag_query_parser.add_argument("--top-k", "-k", type=int, help="Number of results to return")
    
    # RAG stats command
    rag_stats_parser = rag_subparsers.add_parser("stats", help="Get RAG statistics")
    
    # RAG clear command
    rag_clear_parser = rag_subparsers.add_parser("clear", help="Clear the RAG index")
    
    # Workflow commands
    workflow_parser = subparsers.add_parser("workflow", help="Workflow-related commands")
    workflow_subparsers = workflow_parser.add_subparsers(dest="workflow_command", help="Workflow command to execute")
    
    # Workflow create command
    workflow_create_parser = workflow_subparsers.add_parser("create", help="Create a new workflow")
    workflow_create_parser.add_argument("--name", "-n", help="Workflow name")
    workflow_create_parser.add_argument("--files", "-f", nargs="+", help="Input files for the workflow")
    
    # Workflow list command
    workflow_list_parser = workflow_subparsers.add_parser("list", help="List all workflows")
    
    # Workflow status command
    workflow_status_parser = workflow_subparsers.add_parser("status", help="Get workflow status")
    workflow_status_parser.add_argument("--workflow-id", "-w", help="Workflow ID")
    
    # Workflow advance command
    workflow_advance_parser = workflow_subparsers.add_parser("advance", help="Advance workflow to next phase")
    workflow_advance_parser.add_argument("--workflow-id", "-w", help="Workflow ID")
    workflow_advance_parser.add_argument("--phase", "-p", help="Next phase name")
    
    # Workflow task command
    workflow_task_parser = workflow_subparsers.add_parser("task", help="Send a task to an agent")
    workflow_task_parser.add_argument("--workflow-id", "-w", help="Workflow ID")
    workflow_task_parser.add_argument("--agent-id", "-a", help="Agent ID")
    workflow_task_parser.add_argument("--task-type", "-t", help="Task type")
    workflow_task_parser.add_argument("--description", "-d", help="Task description")
    workflow_task_parser.add_argument("--input-data", "-i", help="Task input data (JSON)")
    
    # Workflow finalize command
    workflow_finalize_parser = workflow_subparsers.add_parser("finalize", help="Finalize a workflow")
    workflow_finalize_parser.add_argument("--workflow-id", "-w", help="Workflow ID")
    
    # LLM commands
    llm_parser = subparsers.add_parser("llm", help="LLM-related commands")
    llm_subparsers = llm_parser.add_subparsers(dest="llm_command", help="LLM command to execute")
    
    # LLM generate command
    llm_generate_parser = llm_subparsers.add_parser("generate", help="Generate text using the LLM")
    llm_generate_parser.add_argument("--prompt", "-p", help="Prompt string (if not provided, will read from stdin)")
    llm_generate_parser.add_argument("--model", "-m", help="Model name")
    llm_generate_parser.add_argument("--temperature", "-t", type=float, help="Temperature")
    llm_generate_parser.add_argument("--max-tokens", "-k", type=int, help="Max tokens")
    
    # LLM agent-prompt command
    llm_agent_prompt_parser = llm_subparsers.add_parser("agent-prompt", help="Generate text using an agent's prompt template")
    llm_agent_prompt_parser.add_argument("--agent-id", "-a", help="Agent ID")
    llm_agent_prompt_parser.add_argument("--prompt-type", "-t", help="Prompt type")
    llm_agent_prompt_parser.add_argument("--variables", "-v", help="Variables for the prompt (JSON)")
    llm_agent_prompt_parser.add_argument("--model", "-m", help="Model name")
    llm_agent_prompt_parser.add_argument("--temperature", "-temp", type=float, help="Temperature")
    llm_agent_prompt_parser.add_argument("--max-tokens", "-k", type=int, help="Max tokens")
    
    # LLM templates command
    llm_templates_parser = llm_subparsers.add_parser("templates", help="List available prompt templates")
    llm_templates_parser.add_argument("--agent-id", "-a", help="Agent ID to get templates for")
    
    # Demo commands
    demo_parser = subparsers.add_parser("demo", help="Demo-related commands")
    demo_subparsers = demo_parser.add_subparsers(dest="demo_command", help="Demo command to execute")
    
    # Demo setup command
    demo_setup_parser = demo_subparsers.add_parser("setup", help="Set up the demo environment")
    
    # Demo workflow command
    demo_workflow_parser = demo_subparsers.add_parser("workflow", help="Run a sample workflow")
    
    return parser

async def main():
    """Main entry point."""
    parser = setup_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "rag":
        if not args.rag_command:
            parser.parse_args(["rag", "--help"])
            return
        
        await handle_rag_commands(args)
        
    elif args.command == "workflow":
        if not args.workflow_command:
            parser.parse_args(["workflow", "--help"])
            return
        
        await handle_workflow_commands(args)
        
    elif args.command == "llm":
        if not args.llm_command:
            parser.parse_args(["llm", "--help"])
            return
        
        await handle_llm_commands(args)
        
    elif args.command == "demo":
        if not args.demo_command:
            parser.parse_args(["demo", "--help"])
            return
        
        await handle_demo_commands(args)

if __name__ == "__main__":
    asyncio.run(main())