"""
Integration tests for the RAG service.

These tests ensure that the different components of the RAG system
work together correctly.
"""

import os
import unittest
import tempfile
from pathlib import Path
import json
import shutil

# Add project root to Python path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.utils.document_processor import DocumentProcessor
from src.utils.embeddings import VectorStoreManager
from src.services.rag_service import RagService


class TestRAGIntegration(unittest.TestCase):
    """Integration tests for the RAG service."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for the vector store
        self.test_dir = tempfile.mkdtemp()
        self.vector_db_path = os.path.join(self.test_dir, "vectordb")
        
        # Create test document files
        self.docs_dir = os.path.join(self.test_dir, "docs")
        os.makedirs(self.docs_dir, exist_ok=True)
        
        # Create a test text document
        self.test_txt = os.path.join(self.docs_dir, "architecture.txt")
        with open(self.test_txt, "w") as f:
            f.write("""Microservices Architecture

Microservices architecture is an architectural style that structures an application as a collection of small, loosely coupled services. Each service is focused on a specific business capability and can be developed, deployed, and scaled independently.

Key characteristics of microservices architecture:
1. Services are organized around business capabilities
2. Each service has its own database
3. Services communicate via lightweight protocols (often HTTP/REST)
4. Services can be implemented in different programming languages
5. Services are independently deployable
6. Decentralized governance and data management
""")
        
        # Create a test markdown document
        self.test_md = os.path.join(self.docs_dir, "api_design.md")
        with open(self.test_md, "w") as f:
            f.write("""# API Design Best Practices

## RESTful API Guidelines

- Use nouns instead of verbs in endpoint paths
- Use logical nesting for resources
- Use HTTP methods appropriately (GET, POST, PUT, DELETE)
- Return appropriate status codes
- Implement proper error handling

## GraphQL Considerations

- Consider GraphQL for complex data requirements
- Implement proper error handling
- Optimize resolver performance
""")
        
        # Create instances of the components
        self.document_processor = DocumentProcessor(chunk_size=200, chunk_overlap=20)
        self.vector_store = VectorStoreManager(db_directory=self.vector_db_path)
        
        # Create the RAG service with the test vector DB path
        self.rag_service = RagService(
            vector_db_path=self.vector_db_path,
            chunk_size=200,
            chunk_overlap=20,
            similarity_top_k=3
        )
    
    def tearDown(self):
        """Clean up test environment."""
        # Remove test directories
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_end_to_end_indexing_and_querying(self):
        """Test the complete RAG pipeline from indexing to querying."""
        # Index the test documents
        file_paths = [self.test_txt, self.test_md]
        index_result = self.rag_service.index_documents(file_paths, collection_name="test_collection")
        
        # Verify indexing result
        self.assertEqual(index_result["status"], "success")
        self.assertGreater(index_result["document_count"], 0)
        self.assertIn("metadata", index_result)
        self.assertIn("vector_store_stats", index_result)
        
        # Query for microservices information
        micro_query = "What are the key characteristics of microservices architecture?"
        micro_results = self.rag_service.retrieve_documents(micro_query)
        
        # Verify microservices query results
        self.assertGreater(len(micro_results), 0)
        found_micro = False
        for doc in micro_results:
            if "microservices" in doc["content"].lower():
                found_micro = True
                break
        self.assertTrue(found_micro, "Did not find microservices in query results")
        
        # Query for API design information
        api_query = "What are the best practices for RESTful API design?"
        api_results = self.rag_service.retrieve_documents(api_query)
        
        # Verify API query results
        self.assertGreater(len(api_results), 0)
        found_api = False
        for doc in api_results:
            if "api" in doc["content"].lower() or "rest" in doc["content"].lower():
                found_api = True
                break
        self.assertTrue(found_api, "Did not find API in query results")
    
    def test_agent_specific_context(self):
        """Test getting agent-specific context."""
        # Index the test documents
        file_paths = [self.test_txt, self.test_md]
        self.rag_service.index_documents(file_paths, collection_name="test_collection")
        
        # Get context for SAA agent
        query = "How should I design APIs?"
        saa_context = self.rag_service.get_context_for_agent(query, "SAA")
        
        # Verify SAA context
        self.assertEqual(saa_context["agent_type"], "SAA")
        self.assertEqual(saa_context["query"], query)
        self.assertIn("enhanced_query", saa_context)
        self.assertIn("system architecture design concepts for:", saa_context["enhanced_query"])
        self.assertGreater(len(saa_context["documents"]), 0)
        
        # Get context for RAA agent
        raa_context = self.rag_service.get_context_for_agent(query, "RAA")
        
        # Verify RAA context
        self.assertEqual(raa_context["agent_type"], "RAA")
        self.assertEqual(raa_context["query"], query)
        self.assertIn("enhanced_query", raa_context)
        self.assertIn("requirements analysis for:", raa_context["enhanced_query"])
        self.assertGreater(len(raa_context["documents"]), 0)
    
    def test_generate_response(self):
        """Test generating a response based on retrieved documents."""
        # Index the test documents
        file_paths = [self.test_txt, self.test_md]
        self.rag_service.index_documents(file_paths, collection_name="test_collection")
        
        # Retrieve documents
        query = "What is microservices architecture?"
        documents = self.rag_service.retrieve_documents(query)
        
        # Generate response
        response = self.rag_service.generate_response(query, documents, "SAA")
        
        # Verify response
        self.assertEqual(response.query, query)
        self.assertGreater(len(response.retrieved_documents), 0)
        self.assertIsNotNone(response.answer)
        self.assertGreater(len(response.source_documents), 0)
    
    def test_complete_query(self):
        """Test the complete query method."""
        # Index the test documents
        file_paths = [self.test_txt, self.test_md]
        self.rag_service.index_documents(file_paths, collection_name="test_collection")
        
        # Perform a complete query
        query = "What is microservices architecture?"
        result = self.rag_service.query(query, agent_type="SAA")
        
        # Verify result
        self.assertEqual(result.query, query)
        self.assertGreater(len(result.retrieved_documents), 0)
        self.assertIsNotNone(result.answer)
        self.assertGreater(len(result.source_documents), 0)


if __name__ == "__main__":
    unittest.main()