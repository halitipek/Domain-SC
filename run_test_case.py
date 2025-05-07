#!/usr/bin/env python
"""
Test case runner for Domain-SC.

This script processes real-world test cases through the RAG-enhanced
multi-agent system and generates architecture documentation.
"""

import os
import sys
import argparse
import json
import logging
from datetime import datetime
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

from src.utils.logger import setup_logger
from src.services.rag_service import RagService
from src.services.workflow_service import WorkflowService
from src.utils.document_processor import DocumentProcessor

# Set up logging
logger = setup_logger(__name__, "test_case_runner.log")

def process_test_case(test_case_dir: str, output_dir: str = None, debug: bool = False):
    """Process a test case directory through the system.
    
    Args:
        test_case_dir: Path to the test case directory
        output_dir: Path to the output directory (default: data/output/{timestamp})
        debug: Enable debug mode with extra logging
    """
    # Setup logging level
    if debug:
        logger.setLevel(logging.DEBUG)
    
    # Validate test case directory
    test_case_path = Path(test_case_dir)
    if not test_case_path.exists() or not test_case_path.is_dir():
        logger.error(f"Test case directory {test_case_dir} does not exist or is not a directory")
        return False
        
    # Set up output directory
    if output_dir is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join("data", "output", f"run_{timestamp}")
        
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Processing test case from {test_case_dir}")
    logger.info(f"Output will be saved to {output_dir}")
    
    # List input files
    input_files = []
    for ext in [".txt", ".md", ".pdf", ".json"]:
        input_files.extend(list(test_case_path.glob(f"*{ext}")))
    
    if not input_files:
        logger.error(f"No input files found in {test_case_dir}")
        return False
        
    logger.info(f"Found {len(input_files)} input files")
    for file in input_files:
        logger.info(f"  - {file.name}")
    
    try:
        # Initialize services
        doc_processor = DocumentProcessor()
        rag_service = RagService()
        workflow_service = WorkflowService()
        
        # Process documents
        logger.info("Processing documents...")
        chunked_docs, metadata = doc_processor.process_files([str(f) for f in input_files])
        
        # Save metadata
        with open(os.path.join(output_dir, "metadata.json"), "w") as f:
            json.dump(metadata, f, indent=2)
            
        # Index documents for RAG
        logger.info("Indexing documents for RAG...")
        rag_result = rag_service.index_documents(
            [str(f) for f in input_files],
            collection_name=f"test_case_{datetime.now().strftime('%Y%m%d')}"
        )
        
        # Save RAG results
        with open(os.path.join(output_dir, "rag_index_result.json"), "w") as f:
            json.dump(rag_result, f, indent=2)
        
        # Initialize workflow
        logger.info("Initializing workflow...")
        workflow = workflow_service.initialize_workflow(
            workflow_name=f"test_case_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            input_files=[str(f) for f in input_files]
        )
        
        # Run basic query test
        logger.info("Testing RAG query...")
        query_result = rag_service.query(
            query="What is the main architecture approach?",
            agent_type="SAA"
        )
        
        # Save query result
        with open(os.path.join(output_dir, "query_result.json"), "w") as f:
            json.dump({
                "query": query_result.query,
                "enhanced_query": query_result.enhanced_query,
                "answer": query_result.answer,
                "sources_count": len(query_result.sources) if hasattr(query_result, "sources") else 0
            }, f, indent=2)
        
        logger.info("Test case processing completed successfully")
        logger.info(f"Results saved to {output_dir}")
        return True
        
    except Exception as e:
        logger.error(f"Error processing test case: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False
        
def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run a test case through the Domain-SC system")
    parser.add_argument(
        "test_case_dir",
        help="Path to the test case directory containing input files"
    )
    parser.add_argument(
        "--output-dir", "-o",
        help="Path to the output directory (default: data/output/{timestamp})"
    )
    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Enable debug mode with extra logging"
    )
    
    args = parser.parse_args()
    
    success = process_test_case(
        test_case_dir=args.test_case_dir,
        output_dir=args.output_dir,
        debug=args.debug
    )
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()