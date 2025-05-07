#!/usr/bin/env python
"""
Test script to verify the module imports for the Domain-SC system.
This helps identify any issues with Python paths or missing dependencies.
"""

import os
import sys
import importlib
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

# Also add the src directory to the path
src_path = os.path.join(project_root, "src")
sys.path.append(str(src_path))

def test_import(module_path):
    """Test importing a specific module."""
    try:
        # Try the import
        module = importlib.import_module(module_path)
        print(f"✅ Successfully imported {module_path}")
        return True
    except ImportError as e:
        print(f"❌ Failed to import {module_path}: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error when importing {module_path}: {str(e)}")
        return False

def main():
    """Run import tests for key components."""
    print("Testing Domain-SC module imports...\n")
    
    # List of modules to test
    modules_to_test = [
        # Core modules
        "services.llm_service",
        "services.rag_service",
        "services.optimized_llm_service",
        "services.enhanced_rag_service",
        "agents.system_architect_agent",
        "agents.enhanced_system_architect_agent",
        "prompts.adaptive_prompt_system",
    ]
    
    # Track overall success
    success_count = 0
    total_count = len(modules_to_test)
    
    # Run tests
    for module in modules_to_test:
        if test_import(module):
            success_count += 1
    
    # Print summary
    print(f"\nModule import test complete: {success_count}/{total_count} successful")
    
    if success_count == total_count:
        print("\nAll module imports are working correctly! ✅")
        print("You can proceed with running the integration script.")
    else:
        print("\nSome module imports failed. ❌")
        print("Please check the Python path and ensure all dependencies are installed.")
        print("You might need to run: pip install -r requirements.txt")
    
    # Verify key files
    print("\nVerifying key files:")
    key_files = [
        "src/services/optimized_llm_service.py",
        "src/services/enhanced_rag_service.py",
        "src/prompts/adaptive_prompt_system.py",
        "src/agents/enhanced_system_architect_agent.py"
    ]
    
    for file_path in key_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")

if __name__ == "__main__":
    main()