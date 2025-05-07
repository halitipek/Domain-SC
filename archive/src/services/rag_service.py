import os
import json
import logging
from typing import List, Dict, Any, Optional, Union
from pathlib import Path

from src.config.config import RAG_SETTINGS
from src.utils.logger import setup_logger
from src.utils.document_processor import DocumentProcessor
from src.utils.embeddings import VectorStoreManager
from src.models.base_models import Document, RagQueryResult

logger = setup_logger(__name__, "rag_service.log")

class RagService:
    """RAG (Retrieval Augmented Generation) service for the multi-agent system."""
    
    def __init__(self, vector_db_path: str = None, 
                 chunk_size: int = None, 
                 chunk_overlap: int = None,
                 embedding_model: str = None,
                 similarity_top_k: int = None):
        # Load settings from config, override with provided values if any
        self.vector_db_path = vector_db_path or RAG_SETTINGS.get("vector_db_path")
        self.chunk_size = chunk_size or RAG_SETTINGS.get("chunk_size")
        self.chunk_overlap = chunk_overlap or RAG_SETTINGS.get("chunk_overlap")
        self.embedding_model = embedding_model or RAG_SETTINGS.get("embedding_model")
        self.similarity_top_k = similarity_top_k or RAG_SETTINGS.get("similarity_top_k")
        
        # Initialize processors
        self.document_processor = DocumentProcessor(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        
        self.vector_store = VectorStoreManager(
            db_directory=self.vector_db_path,
            embedding_model=self.embedding_model
        )
        
        logger.info(f"RAG Service initialized with vector DB at {self.vector_db_path}")
    
    def index_documents(self, file_paths: List[str], collection_name: Optional[str] = None) -> Dict[str, Any]:
        """Process and index documents for retrieval."""
        # Process documents
        chunked_docs, metadata = self.document_processor.process_files(file_paths)
        
        if not chunked_docs:
            logger.warning(f"No documents were processed from {len(file_paths)} files")
            return {"status": "error", "message": "No documents processed", "metadata": metadata}
        
        # Add to vector store
        self.vector_store.add_documents(chunked_docs, collection_name=collection_name)
        
        # Get stats after indexing
        stats = self.vector_store.get_collection_stats()
        
        result = {
            "status": "success",
            "document_count": len(chunked_docs),
            "metadata": metadata,
            "vector_store_stats": stats
        }
        
        logger.info(f"Indexed {len(chunked_docs)} document chunks from {len(file_paths)} files")
        return result
    
    def retrieve_documents(self, query: str, k: int = None) -> List[Dict[str, Any]]:
        """Retrieve relevant documents for a query.
        
        Args:
            query: The search query
            k: Number of documents to retrieve (default from config)
            
        Returns:
            List of retrieved documents
        """
        if not query:
            logger.warning("Empty query provided to retrieve_documents")
            return []
            
        top_k = k or self.similarity_top_k
        if not isinstance(top_k, int) or top_k <= 0:
            logger.warning(f"Invalid k value: {top_k}, using default 5")
            top_k = 5
            
        try:
            documents = self.vector_store.similar_documents(query, k=top_k)
            
            # Truncate query for logging if it's too long
            log_query = f"{query[:50]}..." if len(query) > 50 else query
            logger.info(f"Retrieved {len(documents)} documents for query: {log_query}")
            return documents
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            return []
    
    def get_context_for_agent(self, query: str, agent_type: str, k: int = None) -> Dict[str, Any]:
        """Get specialized context based on agent type."""
        # Customize the query based on agent type to improve retrieval
        enhanced_query = query
        
        # Enhance query based on agent type
        if agent_type == "SAA":  # System Architect Agent
            enhanced_query = f"system architecture design concepts for: {query}"
        elif agent_type == "RAA":  # Requirements Analysis Agent
            enhanced_query = f"requirements analysis for: {query}"
        elif agent_type == "TAA":  # Technology Analysis Agent
            enhanced_query = f"technology solutions for: {query}"
        elif agent_type == "OAA":  # Optimization Analysis Agent
            enhanced_query = f"optimization strategies for: {query}"
            
        # Retrieve documents
        documents = self.retrieve_documents(enhanced_query, k=k)
        
        # Filter or re-rank based on agent type if needed
        # For example, prioritize architecture patterns for SAA
        
        # Create context object with relevant documents
        context = {
            "query": query,
            "enhanced_query": enhanced_query,
            "agent_type": agent_type,
            "documents": documents,
            "document_count": len(documents)
        }
        
        return context
    
    def generate_response(self, query: str, documents: List[Dict[str, Any]], 
                          agent_type: str = None) -> RagQueryResult:
        """Generate a response based on retrieved documents.
        
        In a production environment, this would call an LLM. For now, we'll
        simulate a simple response.
        """
        # Build a simple response using information from the documents
        # In production, this would be processed by an LLM
        
        # Extract content from documents
        contents = [doc.get("content", "") for doc in documents]
        sources = [doc.get("metadata", {}) for doc in documents]
        
        # Simple template response - in a real system, this would be generated by an LLM
        response = f"Response for query: {query}\n\nBased on {len(documents)} documents"
        
        result = RagQueryResult(
            query=query,
            retrieved_documents=[Document(content=content, metadata={}) for content in contents],
            answer=response,
            source_documents=sources
        )
        
        return result
    
    def query(self, query: str, agent_type: Optional[str] = None, k: Optional[int] = None) -> RagQueryResult:
        """Complete RAG pipeline: retrieve documents and generate response.
        
        Args:
            query: The user query
            agent_type: Optional agent type for specialized context
            k: Optional number of documents to retrieve
            
        Returns:
            RagQueryResult object with the query results
        """
        if not query or not isinstance(query, str):
            logger.error(f"Invalid query: {type(query)}")
            return RagQueryResult(
                query=str(query) if query else "",
                retrieved_documents=[],
                answer="Error: Invalid query",
                source_documents=[]
            )
            
        # Validate k if provided
        if k is not None and (not isinstance(k, int) or k <= 0):
            logger.warning(f"Invalid k value: {k}, using default")
            k = self.similarity_top_k
        
        try:
            # Get context (retrieved documents)
            context = self.get_context_for_agent(query, agent_type, k)
            if not context or not isinstance(context, dict):
                logger.error(f"Invalid context returned for query: {type(context)}")
                return RagQueryResult(
                    query=query,
                    retrieved_documents=[],
                    answer="Error: Failed to retrieve context",
                    source_documents=[]
                )
                
            documents = context.get("documents", [])
            
            # Generate response
            result = self.generate_response(query, documents, agent_type)
            
            logger.info(f"RAG query completed for agent type {agent_type} with {len(documents)} retrieved documents")
            return result
            
        except Exception as e:
            logger.error(f"Error in RAG query pipeline: {str(e)}")
            return RagQueryResult(
                query=query,
                retrieved_documents=[],
                answer=f"Error in RAG pipeline: {str(e)}",
                source_documents=[]
            )
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the RAG service."""
        vector_store_stats = self.vector_store.get_collection_stats()
        
        return {
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "embedding_model": self.embedding_model,
            "similarity_top_k": self.similarity_top_k,
            "vector_store": vector_store_stats
        }
    
    def clear_index(self) -> None:
        """Clear the vector store index."""
        self.vector_store.clear()
        logger.info("RAG service index cleared")
