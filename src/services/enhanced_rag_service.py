"""
Enhanced RAG Service for Domain-SC.
This service improves the RAG capabilities with semantic pre-evaluation to reduce LLM token usage.
"""

import os
import logging
import json
import hashlib
from typing import List, Dict, Any, Optional
import numpy as np
from datetime import datetime

from config.config import RAG_SETTINGS
from utils.logger import setup_logger
from services.optimized_llm_service import OptimizedLLMService

logger = setup_logger(__name__, "rag_service.log")

class EnhancedRAGService:
    """Enhanced RAG service with pre-evaluation capabilities."""
    
    def __init__(self, vector_db_path=None, llm_service=None):
        """Initialize the enhanced RAG service."""
        self.vector_db_path = vector_db_path or RAG_SETTINGS.get("vector_db_path")
        self.chunk_size = RAG_SETTINGS.get("chunk_size", 1000)
        self.chunk_overlap = RAG_SETTINGS.get("chunk_overlap", 200)
        self.embedding_model = RAG_SETTINGS.get("embedding_model")
        self.similarity_top_k = RAG_SETTINGS.get("similarity_top_k", 5)
        
        # Use provided LLM service or create a lightweight one for pre-evaluation
        self.llm_service = llm_service or OptimizedLLMService()
        self.lightweight_llm = self._setup_lightweight_llm()
        
        # Initialize vector store
        self.vector_store = self._initialize_vector_store()
        
        # Relevance cache to avoid repeated evaluations
        self.relevance_cache = {}
        self.cache_ttl = 3600 * 24  # 24 hours
        
        logger.info("Enhanced RAG Service initialized")
    
    def _setup_lightweight_llm(self):
        """Set up lightweight LLM for pre-evaluation."""
        # Create a version of LLM service optimized for quick, cheap evaluations
        # Using a smaller model with lower max_tokens for quick filtering tasks
        lightweight_llm = OptimizedLLMService()
        
        # If we're using GPT-4, downgrade to GPT-3.5 for lightweight evaluations
        if "gpt-4" in lightweight_llm.model:
            lightweight_llm.model = "gpt-3.5-turbo"
        
        # If we're using Claude-3-Opus, downgrade to Claude-3-Haiku
        if "opus" in lightweight_llm.model:
            lightweight_llm.model = "claude-3-haiku"
            
        return lightweight_llm
    
    def _initialize_vector_store(self):
        """Initialize the vector store."""
        try:
            import chromadb
            from chromadb.config import Settings
            
            # Create client
            client = chromadb.PersistentClient(
                path=self.vector_db_path,
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Get or create collection
            collections = client.list_collections()
            collection_names = [c.name for c in collections]
            
            if "domain_sc_kb" in collection_names:
                vector_store = client.get_collection("domain_sc_kb")
                logger.info(f"Using existing vector store with {vector_store.count()} documents")
            else:
                vector_store = client.create_collection(
                    name="domain_sc_kb",
                    metadata={"description": "Domain-SC knowledge base"}
                )
                logger.info("Created new vector store")
            
            return vector_store
        except Exception as e:
            logger.error(f"Error initializing vector store: {str(e)}")
            return None
    
    def pre_evaluate_relevance(self, query: str, document: Dict[str, Any]) -> float:
        """Evaluate document relevance using lightweight LLM."""
        # Create cache key from query and document ID
        doc_id = document.get("id", "")
        cache_key = f"{query[:100]}_{doc_id}"
        
        # Check cache
        if cache_key in self.relevance_cache:
            timestamp, score = self.relevance_cache[cache_key]
            # Check if cache entry is still valid
            if (datetime.now().timestamp() - timestamp) < self.cache_ttl:
                return score
        
        # Create concise relevance evaluation prompt
        content = document.get("document", document.get("text", ""))
        # Only use the first 300 characters for quick assessment
        content_preview = content[:300] + ("..." if len(content) > 300 else "")
        
        prompt = f"""Rate the relevance of this document to the query on a scale of 0-10.
Query: {query}
Document preview: {content_preview}
Focus only on direct relevance. Return only a number from 0 to 10."""
        
        try:
            # Get relevance score from lightweight model
            response = self.lightweight_llm.generate_text(
                prompt=prompt, 
                use_cache=True
            )
            
            # Extract numeric score
            score = 0.0
            for word in response.split():
                try:
                    extracted_score = float(word.strip())
                    if 0 <= extracted_score <= 10:
                        score = extracted_score / 10.0  # Normalize to 0-1
                        break
                except ValueError:
                    continue
            
            # Cache the result
            self.relevance_cache[cache_key] = (datetime.now().timestamp(), score)
            return score
            
        except Exception as e:
            logger.warning(f"Error evaluating relevance: {str(e)}")
            return 0.5  # Default to middle score on error
    
    def semantic_retrieval(self, query: str, min_relevance: float = 0.45, max_candidates: int = 15) -> List[Dict[str, Any]]:
        """Retrieve documents with semantic pre-evaluation."""
        if not self.vector_store:
            logger.error("Vector store not initialized")
            return []
        
        try:
            # Initial broader retrieval
            results = self.vector_store.query(
                query_texts=[query],
                n_results=max_candidates
            )
            
            documents = []
            ids = results.get("ids", [[]])[0]
            metadatas = results.get("metadatas", [[]])[0]
            documents_content = results.get("documents", [[]])[0]
            distances = results.get("distances", [[]])[0]
            
            # Combine into documents
            candidates = []
            for i in range(len(ids)):
                doc = {
                    "id": ids[i],
                    "metadata": metadatas[i],
                    "document": documents_content[i],
                    "distance": distances[i] if distances else 0.0
                }
                candidates.append(doc)
            
            # Pre-evaluate for relevance
            relevant_docs = []
            for doc in candidates:
                relevance = self.pre_evaluate_relevance(query, doc)
                if relevance >= min_relevance:
                    doc["relevance"] = relevance
                    relevant_docs.append(doc)
            
            # Sort by relevance score
            relevant_docs.sort(key=lambda x: x.get("relevance", 0.0), reverse=True)
            
            # Take top k most relevant docs
            top_k = min(len(relevant_docs), self.similarity_top_k)
            return relevant_docs[:top_k]
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            return []
    
    def retrieve_for_query(self, query: str, min_relevance: float = 0.45) -> List[Dict[str, Any]]:
        """Retrieve documents relevant to a query with optimized processing."""
        # Enhanced query to focus on architecture patterns
        enhanced_query = self._enhance_query(query)
        
        # Retrieve relevant documents
        relevant_docs = self.semantic_retrieval(enhanced_query, min_relevance=min_relevance)
        
        # Log retrieval metrics
        logger.info(f"Retrieved {len(relevant_docs)} relevant documents for query")
        
        return relevant_docs
    
    def _enhance_query(self, query: str) -> str:
        """Enhance the query to improve retrieval quality."""
        if "architecture" not in query.lower() and "design" not in query.lower():
            enhanced = f"system architecture design concepts for: {query}"
            return enhanced
        return query
        
    def index_documents(self, file_paths: List[str], collection_name: str = "domain_sc_kb") -> Dict[str, Any]:
        """Index documents for RAG retrieval."""
        logger.info(f"Indexing {len(file_paths)} documents")
        
        try:
            # Create or get collection
            import chromadb
            from chromadb.config import Settings
            
            client = chromadb.PersistentClient(
                path=self.vector_db_path,
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Check if collection exists
            collections = client.list_collections()
            collection_names = [c.name for c in collections]
            
            if collection_name in collection_names:
                collection = client.get_collection(collection_name)
                logger.info(f"Using existing collection: {collection_name}")
            else:
                collection = client.create_collection(
                    name=collection_name,
                    metadata={"description": "Domain-SC knowledge base"}
                )
                logger.info(f"Created new collection: {collection_name}")
            
            # Process and index documents
            from utils.document_processor import process_files
            
            documents, metadatas, ids = process_files(file_paths, self.chunk_size, self.chunk_overlap)
            
            if documents:
                # Add documents to the collection
                collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                logger.info(f"Indexed {len(documents)} document chunks")
                return {
                    "status": "success",
                    "indexed_count": len(documents),
                    "collection": collection_name
                }
            else:
                logger.warning("No documents were processed for indexing")
                return {
                    "status": "warning",
                    "indexed_count": 0,
                    "message": "No documents were processed"
                }
                
        except Exception as e:
            logger.error(f"Error indexing documents: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }