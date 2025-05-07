"""
Workflow-related commands for the Domain-SC CLI.
"""

import argparse
import json
import os
from typing import Any, Dict, List, Optional
from pathlib import Path

from src.services.workflow_service import WorkflowService
from src.utils.logger import setup_logger

# Set up logging
logger = setup_logger("cli.workflow")


def register_commands(subparsers: argparse._SubParsersAction) -> None:
    """
    Register workflow-related commands.
    
    Args:
        subparsers: Subparser group to add to
    """
    # Workflow command group
    workflow_parser = subparsers.add_parser("workflow", help="Workflow-related commands")
    workflow_subparsers = workflow_parser.add_subparsers(dest="workflow_command", help="Workflow command to execute")
    
    # Workflow create command
    workflow_create_parser = workflow_subparsers.add_parser("create", help="Create a new workflow")
    workflow_create_parser.add_argument("--name", "-n", required=True, help="Workflow name")
    workflow_create_parser.add_argument("--files", "-f", nargs="+", required=True, help="Input files for the workflow")
    workflow_create_parser.add_argument("--output-dir", "-o", help="Output directory for workflow artifacts")
    
    # Workflow list command
    workflow_subparsers.add_parser("list", help="List all workflows")
    
    # Workflow status command
    workflow_status_parser = workflow_subparsers.add_parser("status", help="Get workflow status")
    workflow_status_parser.add_argument("--workflow-id", "-w", required=True, help="Workflow ID")
    
    # Workflow advance command
    workflow_advance_parser = workflow_subparsers.add_parser("advance", help="Advance workflow to next phase")
    workflow_advance_parser.add_argument("--workflow-id", "-w", required=True, help="Workflow ID")
    workflow_advance_parser.add_argument("--phase", "-p", required=True, help="Next phase name")
    
    # Workflow task command
    workflow_task_parser = workflow_subparsers.add_parser("task", help="Send a task to an agent")
    workflow_task_parser.add_argument("--workflow-id", "-w", required=True, help="Workflow ID")
    workflow_task_parser.add_argument("--agent-id", "-a", required=True, help="Agent ID")
    workflow_task_parser.add_argument("--task-type", "-t", required=True, help="Task type")
    workflow_task_parser.add_argument("--description", "-d", required=True, help="Task description")
    workflow_task_parser.add_argument("--input-file", "-i", help="JSON file containing input data")
    workflow_task_parser.add_argument("--input-json", "-j", help="Task input data (JSON string)")
    
    # Workflow finalize command
    workflow_finalize_parser = workflow_subparsers.add_parser("finalize", help="Finalize a workflow")
    workflow_finalize_parser.add_argument("--workflow-id", "-w", required=True, help="Workflow ID")
    workflow_finalize_parser.add_argument("--output-dir", "-o", help="Output directory for finalized artifacts")
    
    # Workflow export command
    workflow_export_parser = workflow_subparsers.add_parser("export", help="Export workflow results")
    workflow_export_parser.add_argument("--workflow-id", "-w", required=True, help="Workflow ID")
    workflow_export_parser.add_argument("--output-dir", "-o", required=True, help="Output directory")
    workflow_export_parser.add_argument("--format", "-f", choices=["json", "md", "all"], default="all", 
                                        help="Output format (default: all)")


def print_json(data: Any) -> None:
    """
    Print data as formatted JSON.
    
    Args:
        data: Data to print
    """
    print(json.dumps(data, indent=2))


async def handle_commands(args: argparse.Namespace, config: Any) -> int:
    """
    Handle workflow-related commands.
    
    Args:
        args: Parsed command line arguments
        config: CLI configuration
        
    Returns:
        int: Exit code (0 for success, non-zero for error)
    """
    # Initialize service
    workflow_service = WorkflowService(
        output_path=config.get("workflow", "output_path")
    )
    
    if args.workflow_command == "create":
        # Get output directory
        output_dir = args.output_dir or config.get("workflow", "output_path")
        os.makedirs(output_dir, exist_ok=True)
        
        # Create workflow
        logger.info(f"Creating workflow '{args.name}' with {len(args.files)} input files")
        result = await workflow_service.initialize_workflow(
            name=args.name,
            input_files=args.files,
            output_dir=output_dir
        )
        
        print_json(result)
        return 0
        
    elif args.workflow_command == "list":
        # List all workflows
        result = await workflow_service.get_workflow_status()
        print_json(result)
        return 0
        
    elif args.workflow_command == "status":
        # Get workflow status
        result = await workflow_service.get_workflow_status(args.workflow_id)
        if "status" in result and result["status"] == "error":
            print(f"Error: {result['message']}")
            return 1
            
        print_json(result)
        return 0
        
    elif args.workflow_command == "advance":
        # Advance workflow to next phase
        logger.info(f"Advancing workflow {args.workflow_id} to phase '{args.phase}'")
        result = await workflow_service.advance_workflow(args.workflow_id, args.phase)
        if "status" in result and result["status"] == "error":
            print(f"Error: {result['message']}")
            return 1
            
        print_json(result)
        return 0
        
    elif args.workflow_command == "task":
        # Prepare input data
        input_data: Dict[str, Any] = {}
        
        if args.input_file:
            # Load input data from file
            try:
                with open(args.input_file, 'r') as f:
                    input_data = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading input file: {e}")
                return 1
        
        elif args.input_json:
            # Parse input JSON string
            try:
                input_data = json.loads(args.input_json)
            except json.JSONDecodeError:
                print("Error: Invalid JSON format for input data.")
                return 1
        
        # Send task
        logger.info(f"Sending task '{args.task_type}' to agent {args.agent_id} in workflow {args.workflow_id}")
        result = await workflow_service.send_direct_task(
            workflow_id=args.workflow_id,
            agent_id=args.agent_id,
            description=args.description,
            task_type=args.task_type,
            input_data=input_data
        )
        
        if "status" in result and result["status"] == "error":
            print(f"Error: {result['message']}")
            return 1
            
        print_json(result)
        return 0
        
    elif args.workflow_command == "finalize":
        # Get output directory
        output_dir = args.output_dir or config.get("workflow", "output_path")
        os.makedirs(output_dir, exist_ok=True)
        
        # Finalize workflow
        logger.info(f"Finalizing workflow {args.workflow_id}")
        result = await workflow_service.finalize_workflow(
            workflow_id=args.workflow_id,
            output_dir=output_dir
        )
        
        if "status" in result and result["status"] == "error":
            print(f"Error: {result['message']}")
            return 1
            
        print_json(result)
        return 0
        
    elif args.workflow_command == "export":
        # Ensure output directory exists
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Export workflow results
        logger.info(f"Exporting workflow {args.workflow_id} to {output_dir}")
        result = await workflow_service.export_workflow_results(
            workflow_id=args.workflow_id,
            output_dir=str(output_dir),
            format=args.format
        )
        
        if "status" in result and result["status"] == "error":
            print(f"Error: {result['message']}")
            return 1
            
        print(f"Workflow results exported to {output_dir}")
        print_json(result)
        return 0
    
    else:
        print("Unknown workflow command. Use 'domain-sc workflow --help' for available commands.")
        return 1