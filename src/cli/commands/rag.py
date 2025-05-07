"""
RAG-related commands for the Domain-SC CLI.
"""

import argparse
import json
from typing import Any, Dict, List, Optional

from src.services.enhanced_rag_service import EnhancedRAGService
from src.utils.logger import setup_logger

# Set up logging
logger = setup_logger("cli.rag")


def register_commands(subparsers: argparse._SubParsersAction) -> None:
    """
    Register RAG-related commands.
    
    Args:
        subparsers: Subparser group to add to
    """
    # RAG command group
    rag_parser = subparsers.add_parser("rag", help="RAG-related commands")
    rag_subparsers = rag_parser.add_subparsers(dest="rag_command", help="RAG command to execute")
    
    # RAG index command
    rag_index_parser = rag_subparsers.add_parser("index", help="Index documents for RAG")
    rag_index_parser.add_argument("--files", "-f", nargs="+", required=True, help="Files to index")
    rag_index_parser.add_argument("--collection", "-c", help="Collection name")
    rag_index_parser.add_argument("--chunk-size", type=int, default=1000, help="Chunk size for document processing")
    rag_index_parser.add_argument("--chunk-overlap", type=int, default=200, help="Chunk overlap size")
    
    # RAG query command
    rag_query_parser = rag_subparsers.add_parser("query", help="Query the RAG system")
    rag_query_parser.add_argument("--query", "-q", required=True, help="Query string")
    rag_query_parser.add_argument("--collection", "-c", help="Collection to query")
    rag_query_parser.add_argument("--top-k", "-k", type=int, help="Number of results to return")
    rag_query_parser.add_argument("--no-pre-eval", action="store_true", help="Disable semantic pre-evaluation")
    
    # RAG stats command
    rag_subparsers.add_parser("stats", help="Get RAG statistics")
    
    # RAG clear command
    rag_clear_parser = rag_subparsers.add_parser("clear", help="Clear the RAG index")
    rag_clear_parser.add_argument("--collection", "-c", help="Collection to clear")
    rag_clear_parser.add_argument("--all", "-a", action="store_true", help="Clear all collections")
    
    # RAG export command
    rag_export_parser = rag_subparsers.add_parser("export", help="Export RAG index")
    rag_export_parser.add_argument("--collection", "-c", required=True, help="Collection to export")
    rag_export_parser.add_argument("--output", "-o", required=True, help="Output file path")
    
    # RAG import command
    rag_import_parser = rag_subparsers.add_parser("import", help="Import RAG index")
    rag_import_parser.add_argument("--input", "-i", required=True, help="Input file path")
    rag_import_parser.add_argument("--collection", "-c", help="Collection name (if different from source)")


def print_json(data: Any) -> None:
    """
    Print data as formatted JSON.
    
    Args:
        data: Data to print
    """
    print(json.dumps(data, indent=2))


async def handle_commands(args: argparse.Namespace, config: Any) -> int:
    """
    Handle RAG-related commands.
    
    Args:
        args: Parsed command line arguments
        config: CLI configuration
        
    Returns:
        int: Exit code (0 for success, non-zero for error)
    """
    # Initialize service
    rag_service = EnhancedRAGService(
        vectordb_path=config.get("rag", "vectordb_path")
    )
    
    if args.rag_command == "index":
        # Get collection name (with default from config if not provided)
        collection = args.collection or config.get("rag", "default_collection")
        
        # Index documents
        logger.info(f"Indexing {len(args.files)} documents into collection '{collection}'")
        result = await rag_service.index_documents(
            file_paths=args.files,
            collection_name=collection,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap
        )
        print_json(result)
        
    elif args.rag_command == "query":
        # Get collection and top_k (with defaults from config if not provided)
        collection = args.collection or config.get("rag", "default_collection")
        top_k = args.top_k or config.get("rag", "default_top_k")
        
        # Query the RAG system
        logger.info(f"Querying collection '{collection}' with: {args.query}")
        result = await rag_service.query(
            query=args.query,
            collection_name=collection,
            top_k=top_k,
            disable_pre_eval=args.no_pre_eval
        )
        print_json(result)
        
    elif args.rag_command == "stats":
        # Get RAG statistics
        stats = await rag_service.get_stats()
        print_json(stats)
        
    elif args.rag_command == "clear":
        # Clear the RAG index
        if args.all:
            logger.info("Clearing all RAG collections")
            await rag_service.clear_all_collections()
            print("All RAG collections cleared successfully.")
        else:
            # Get collection name (with default from config if not provided)
            collection = args.collection or config.get("rag", "default_collection")
            logger.info(f"Clearing RAG collection '{collection}'")
            await rag_service.clear_collection(collection)
            print(f"RAG collection '{collection}' cleared successfully.")
            
    elif args.rag_command == "export":
        # Export RAG index
        logger.info(f"Exporting collection '{args.collection}' to {args.output}")
        await rag_service.export_collection(args.collection, args.output)
        print(f"Collection '{args.collection}' exported to {args.output}")
        
    elif args.rag_command == "import":
        # Import RAG index
        collection = args.collection
        logger.info(f"Importing collection from {args.input}" + 
                    (f" as '{collection}'" if collection else ""))
        await rag_service.import_collection(args.input, collection)
        print(f"Collection imported from {args.input}" + 
              (f" as '{collection}'" if collection else ""))
    
    else:
        print("Unknown RAG command. Use 'domain-sc rag --help' for available commands.")
        return 1
    
    return 0