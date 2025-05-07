#!/usr/bin/env python
"""
Command-line interface for the Domain-SC system.
This module serves as the entry point for the CLI, registering and routing commands.
"""

import argparse
import asyncio
import sys
from typing import Optional
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))

# Import command modules
from src.cli.commands import rag, workflow, llm, demo
from src.cli.config import CliConfig
from src.utils.logger import setup_logger

# Set up logging
logger = setup_logger("cli")


def setup_parser() -> argparse.ArgumentParser:
    """Set up the argument parser with all command groups."""
    parser = argparse.ArgumentParser(
        description="Domain-SC Command Line Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Index documents for RAG:
  domain-sc rag index -f document1.md document2.md -c my_collection
  
  # Query the RAG system:
  domain-sc rag query -q "What is the architecture pattern for high availability?"
  
  # Create a new workflow:
  domain-sc workflow create -n my_workflow -f requirements.md technology.md
  
  # Run a demo workflow:
  domain-sc demo workflow
        """
    )
    
    # Create subparsers for command groups
    subparsers = parser.add_subparsers(dest="command", help="Command group")
    
    # Register command groups
    rag.register_commands(subparsers)
    workflow.register_commands(subparsers)
    llm.register_commands(subparsers)
    demo.register_commands(subparsers)
    
    return parser


async def main(args: Optional[list] = None) -> int:
    """
    Main entry point for the CLI.
    
    Args:
        args: Command line arguments (if None, sys.argv[1:] will be used)
        
    Returns:
        int: Exit code (0 for success, non-zero for error)
    """
    parser = setup_parser()
    parsed_args = parser.parse_args(args)
    
    # Initialize configuration
    config = CliConfig()
    
    if not parsed_args.command:
        parser.print_help()
        return 0
    
    try:
        # Route to appropriate command handler
        if parsed_args.command == "rag":
            if not parsed_args.rag_command:
                parser.parse_args([parsed_args.command, "--help"])
                return 0
            return await rag.handle_commands(parsed_args, config)
            
        elif parsed_args.command == "workflow":
            if not parsed_args.workflow_command:
                parser.parse_args([parsed_args.command, "--help"])
                return 0
            return await workflow.handle_commands(parsed_args, config)
            
        elif parsed_args.command == "llm":
            if not parsed_args.llm_command:
                parser.parse_args([parsed_args.command, "--help"])
                return 0
            return await llm.handle_commands(parsed_args, config)
            
        elif parsed_args.command == "demo":
            if not parsed_args.demo_command:
                parser.parse_args([parsed_args.command, "--help"])
                return 0
            return await demo.handle_commands(parsed_args, config)
        
        else:
            parser.print_help()
            return 0
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1


def run() -> None:
    """Run the CLI application."""
    exit_code = asyncio.run(main())
    sys.exit(exit_code)


if __name__ == "__main__":
    run()