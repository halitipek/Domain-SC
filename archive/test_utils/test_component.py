#!/usr/bin/env python
"""
Simple test script to verify the functionality of individual Domain-SC components.
This script uses direct imports and minimal dependencies to diagnose issues.
"""

import os
import sys
from pathlib import Path

# Set up Python paths
PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(SRC_PATH))

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_llm_service():
    """Test basic LLM service functionality."""
    try:
        logger.info("Importing LLM service...")
        from src.services.llm_service import LLMService
        
        logger.info("Creating LLM service instance...")
        llm_service = LLMService()
        
        logger.info("Testing LLM service generation...")
        prompt = "What is the main advantage of microservices architecture?"
        response = llm_service.generate_text(prompt=prompt)
        
        logger.info(f"Response received: {response[:100]}...")
        return True
    except Exception as e:
        logger.error(f"Error testing LLM service: {str(e)}")
        return False

def test_rag_service():
    """Test basic RAG service functionality."""
    try:
        logger.info("Importing RAG service...")
        from src.services.rag_service import RagService
        
        logger.info("Creating RAG service instance...")
        rag_service = RagService()
        
        logger.info("Testing RAG document access...")
        collections = rag_service.list_collections()
        
        logger.info(f"Available collections: {collections}")
        return True
    except Exception as e:
        logger.error(f"Error testing RAG service: {str(e)}")
        return False

def test_optimized_llm_service():
    """Test optimized LLM service."""
    try:
        logger.info("Importing optimized LLM service...")
        from src.services.optimized_llm_service import OptimizedLLMService
        
        logger.info("Creating optimized LLM service instance...")
        llm_service = OptimizedLLMService()
        
        logger.info("Testing model selection...")
        selected_model = llm_service._select_optimal_model("Test prompt", "low")
        
        logger.info(f"Selected model: {selected_model}")
        return True
    except Exception as e:
        logger.error(f"Error testing optimized LLM service: {str(e)}")
        return False

def test_adaptive_prompt_system():
    """Test adaptive prompt system."""
    try:
        logger.info("Importing adaptive prompt system...")
        from src.prompts.adaptive_prompt_system import AdaptivePromptSystem
        
        logger.info("Creating adaptive prompt system instance...")
        prompt_system = AdaptivePromptSystem()
        
        logger.info("Testing template loading...")
        templates = prompt_system.list_available_templates()
        
        logger.info(f"Available templates: {templates[:5] if templates else 'None'}")
        return True
    except Exception as e:
        logger.error(f"Error testing adaptive prompt system: {str(e)}")
        return False

def main():
    """Run tests for selected components."""
    print("Domain-SC Component Test\n")
    print("This script tests individual components to verify functionality.\n")
    
    print("Available tests:")
    print("1. Basic LLM Service")
    print("2. Basic RAG Service")
    print("3. Optimized LLM Service")
    print("4. Adaptive Prompt System")
    print("5. Run All Tests")
    
    try:
        choice = int(input("\nEnter test number (1-5): "))
        print()
        
        if choice == 1:
            test_llm_service()
        elif choice == 2:
            test_rag_service()
        elif choice == 3:
            test_optimized_llm_service()
        elif choice == 4:
            test_adaptive_prompt_system()
        elif choice == 5:
            print("Running all tests...")
            print("\n1. Basic LLM Service")
            test_llm_service()
            print("\n2. Basic RAG Service")
            test_rag_service()
            print("\n3. Optimized LLM Service")
            test_optimized_llm_service()
            print("\n4. Adaptive Prompt System")
            test_adaptive_prompt_system()
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
    except ValueError:
        print("Please enter a valid number.")
    
    print("\nTests complete.")
    print("If you're seeing error messages, check that all dependencies are installed")
    print("and that the component files exist in the expected locations.")

if __name__ == "__main__":
    main()