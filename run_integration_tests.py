#!/usr/bin/env python
"""
Runner script for the Domain-SC integration tests.
This script sets up the proper Python path and then runs the integration tests.
"""

import os
import sys
import argparse
import importlib.util
from pathlib import Path

# Set up paths
PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"

# Add paths to Python path
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(SRC_PATH))

def run_module(module_path, args=None):
    """Dynamically import and run a module with command line args."""
    try:
        # Get the module spec
        spec = importlib.util.spec_from_file_location("module.name", module_path)
        if spec is None:
            print(f"Failed to find module at {module_path}")
            return False
            
        # Import the module
        module = importlib.util.module_from_spec(spec)
        sys.modules["module.name"] = module
        spec.loader.exec_module(module)
        
        # Run the module main function with args
        if hasattr(module, 'main'):
            if args:
                # Save original args
                orig_args = sys.argv
                # Set new args
                sys.argv = [module_path] + args
                # Run module
                module.main()
                # Restore original args
                sys.argv = orig_args
            else:
                module.main()
            return True
        else:
            print(f"Module {module_path} has no main() function")
            return False
    except Exception as e:
        print(f"Error running {module_path}: {str(e)}")
        return False

def main():
    """Parse arguments and run the tests."""
    parser = argparse.ArgumentParser(description="Run Domain-SC integration tests")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--test-llm", action="store_true", help="Test optimized LLM service")
    parser.add_argument("--test-rag", action="store_true", help="Test enhanced RAG service") 
    parser.add_argument("--test-agent", action="store_true", help="Test enhanced system architect agent")
    parser.add_argument("--compare", action="store_true", help="Compare standard vs enhanced agents")
    parser.add_argument("--create-docs", action="store_true", help="Create documentation")
    
    args = parser.parse_args()
    
    # If no arguments specified, run with --all
    if not any([args.all, args.test_llm, args.test_rag, args.test_agent, args.compare, args.create_docs]):
        args.all = True
    
    # Convert args to list for passing to module
    arg_list = []
    if args.all:
        arg_list.append("--all")
    if args.test_llm:
        arg_list.append("--test-llm")
    if args.test_rag:
        arg_list.append("--test-rag")
    if args.test_agent:
        arg_list.append("--test-agent")
    if args.compare:
        arg_list.append("--compare")
    if args.create_docs:
        arg_list.append("--create-docs")
    
    # Path to integration script
    script_path = SRC_PATH / "integrate_improvements.py"
    
    print(f"Running integration tests with arguments: {' '.join(arg_list)}")
    success = run_module(str(script_path), arg_list)
    
    if success:
        print("\nTests completed successfully!")
    else:
        print("\nThere were errors running the tests.")
        print("Check that all dependencies are installed and properly configured.")

if __name__ == "__main__":
    main()