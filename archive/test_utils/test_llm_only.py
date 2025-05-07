#!/usr/bin/env python
"""
Simple test for the optimized LLM service.
This is a minimal script with absolute imports to test functionality.
"""

import os
import sys
from pathlib import Path

# Set up paths
PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"

# Add paths to Python path
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(SRC_PATH))

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Test the optimized LLM service."""
    print("Loading OptimizedLLMService...")
    
    try:
        from src.services.optimized_llm_service import OptimizedLLMService
        llm = OptimizedLLMService()
        
        print("\nTesting generation with task complexity:")
        prompt = "Explain the advantages of simulation-based architecture design."
        
        # Test different complexity levels
        for complexity in ["low", "medium", "high"]:
            print(f"\nComplexity: {complexity}")
            result = llm.generate_text(prompt=prompt, task_complexity=complexity)
            print(f"Model selected: {llm.model}")
            print(f"Response (first 100 chars): {result[:100]}...")
        
        # Test semantic caching
        print("\nTesting semantic caching:")
        similar_prompt = "What are the benefits of using simulation in architecture design?"
        result = llm.generate_text(prompt=similar_prompt, use_cache=True)
        
        # Get usage stats
        print("\nUsage statistics:")
        stats = llm.get_usage_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        print("\nTest completed successfully!")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    main()