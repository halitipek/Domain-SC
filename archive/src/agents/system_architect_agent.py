import os
import json
import logging
from typing import List, Dict, Any, Optional

from src.agents.base_agent import BaseAgent
from src.services.rag_service import RagService
from src.models.base_models import AgentTask, AgentQuery, AgentResponse
from src.utils.logger import setup_logger

logger = setup_logger(__name__, "system_architect_agent.log")

class SystemArchitectAgent(BaseAgent):
    """System Architect Agent (SAA) enhanced with RAG for architecture knowledge."""
    
    def __init__(self, agent_id: str = "SAA", name: str = "System Architect Agent", 
                 max_tokens: int = 8000):
        super().__init__(agent_id, name, max_tokens)
        
        # Initialize RAG service for architecture knowledge
        self.rag_service = RagService()
        
        # Knowledge areas for the SAA
        self.knowledge_areas = [
            "system architecture",
            "design patterns",
            "data flow modeling",
            "api design",
            "module organization",
            "dependency management",
            "performance optimization",
            "scalability",
            "architectural styles",
            "integration patterns"
        ]
        
        # Track created documents
        self.created_documents = {
            "SMAP": None,  # System Architecture Main Plan
            "APIDF": None,  # API Design Framework
            "MDD": None,  # Module Definition Document
            "DAG": None,  # Dependency Analysis Guide
            "AR": None,  # Architecture Roadmap
            "ADD": None,  # Architecture Design Document
        }
        
        logger.info(f"System Architect Agent initialized")
    
    def execute_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Execute a task by its ID with RAG assistance."""
        if task_id not in self.tasks:
            logger.error(f"Task {task_id} not found for agent {self.agent_id}")
            return None
            
        task = self.tasks[task_id]
        task.status = "in_progress"
        
        logger.info(f"SAA executing task: {task.description}")
        
        result = None
        
        # Handle different task types with RAG assistance
        if task.task_type == "create_architecture_document":
            document_type = task.input_data.get("document_type")
            input_documents = task.input_data.get("input_documents", {})
            
            # Use RAG to help with document creation
            result = self._create_architecture_document(document_type, input_documents)
            
        elif task.task_type == "review_architecture":
            documents = task.input_data.get("documents", {})
            review_criteria = task.input_data.get("review_criteria", [])
            
            # Use RAG to help with architecture review
            result = self._review_architecture(documents, review_criteria)
            
        elif task.task_type == "analyze_dependencies":
            modules = task.input_data.get("modules", [])
            apis = task.input_data.get("apis", [])
            
            # Use RAG to help with dependency analysis
            result = self._analyze_dependencies(modules, apis)
            
        elif task.task_type == "create_complete_add":
            # Final comprehensive architecture document
            input_documents = task.input_data.get("input_documents", {})
            
            # Use RAG to help with final ADD creation
            result = self._create_complete_add(input_documents)
        
        # Update task with result
        if result:
            task.status = "completed"
            task.result = result
        else:
            task.status = "failed"
            task.result = {"error": f"Unknown task type or failed execution: {task.task_type}"}
        
        logger.info(f"SAA completed task {task_id} with status {task.status}")
        return task.result
    
    def process_query(self, query: AgentQuery) -> AgentResponse:
        """Process a query from another agent using RAG for enhanced responses."""
        logger.info(f"SAA processing query from {query.sender}: {query.content[:50]}...")
        
        # Use RAG to get relevant architectural knowledge
        rag_result = self.rag_service.query(query.content, agent_type="SAA")
        
        # Extract relevant documents and create sources list
        sources = [
            {
                "content": doc.content[:200] + "...",  # Truncate for brevity
                "source": doc.metadata.get("source", "unknown")
            } for doc in rag_result.retrieved_documents[:3]  # Top 3 most relevant
        ]
        
        # Create response with RAG-enhanced knowledge
        response_content = f"Based on architectural best practices and the project requirements, here's my analysis:\n\n{rag_result.answer}"
        
        response = AgentResponse(
            query_id=query.query_id,
            sender=self.agent_id,
            recipient=query.sender,
            content=response_content,
            sources=sources
        )
        
        return response
    
    def _create_architecture_document(self, document_type: str, 
                                      input_documents: Dict[str, str]) -> Dict[str, Any]:
        """Create an architecture document with RAG assistance."""
        if document_type not in self.created_documents:
            return {"error": f"Unknown document type: {document_type}"}
            
        logger.info(f"Creating architecture document: {document_type}")
        
        # Use RAG to get relevant architectural knowledge for this document type
        query = f"How to create a {document_type} for a system architecture?"
        rag_result = self.rag_service.query(query, agent_type="SAA")
        
        # In a real implementation, this would use an LLM with the RAG context
        # to generate the actual document content
        
        # For demo purposes, we'll create a placeholder
        document_content = f"{document_type} Document\n\n"
        document_content += f"Created using input from: {', '.join(input_documents.keys())}\n\n"
        document_content += f"RAG Context: Used {len(rag_result.retrieved_documents)} relevant architecture references"
        
        # Store the created document
        self.created_documents[document_type] = document_content
        
        return {
            "status": "success",
            "document_type": document_type,
            "document": document_content
        }
    
    def _review_architecture(self, documents: Dict[str, str], 
                           review_criteria: List[str]) -> Dict[str, Any]:
        """Review architecture documents with RAG assistance."""
        logger.info(f"Reviewing architecture with {len(review_criteria)} criteria")
        
        reviews = {}
        for doc_name, doc_content in documents.items():
            # For each document, use RAG to get relevant review knowledge
            query = f"How to review a {doc_name} architecture document? Criteria: {', '.join(review_criteria)}"
            rag_result = self.rag_service.query(query, agent_type="SAA")
            
            # In a real implementation, this would use an LLM with the RAG context
            # to generate the actual review content
            
            # For demo purposes, we'll create a placeholder
            review_content = f"Review of {doc_name}\n\n"
            review_content += f"Criteria applied: {', '.join(review_criteria)}\n\n"
            review_content += f"RAG Context: Used {len(rag_result.retrieved_documents)} relevant architecture references"
            
            reviews[doc_name] = review_content
        
        return {
            "status": "success",
            "reviews": reviews
        }
    
    def _analyze_dependencies(self, modules: List[Dict[str, Any]], 
                            apis: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze dependencies between modules and APIs with RAG assistance."""
        logger.info(f"Analyzing dependencies for {len(modules)} modules and {len(apis)} APIs")
        
        # Use RAG to get relevant dependency analysis knowledge
        query = f"How to analyze dependencies between {len(modules)} modules and {len(apis)} APIs?"
        rag_result = self.rag_service.query(query, agent_type="SAA")
        
        # In a real implementation, this would use an LLM with the RAG context
        # to generate the actual analysis content
        
        # For demo purposes, we'll create a placeholder
        analysis = f"Dependency Analysis\n\n"
        analysis += f"Analyzed {len(modules)} modules and {len(apis)} APIs\n\n"
        analysis += f"RAG Context: Used {len(rag_result.retrieved_documents)} relevant architecture references"
        
        # Create a dependency matrix (simplified)
        matrix = []
        for module in modules:
            row = {"module": module.get("name", "unknown"), "dependencies": []}
            for api in apis:
                if api.get("name", "") in module.get("uses_apis", []):
                    row["dependencies"].append(api.get("name", "unknown"))
            matrix.append(row)
        
        return {
            "status": "success",
            "analysis": analysis,
            "dependency_matrix": matrix
        }
    
    def _create_complete_add(self, input_documents: Dict[str, str]) -> Dict[str, Any]:
        """Create the final Architecture Design Document with RAG assistance."""
        logger.info(f"Creating complete ADD with {len(input_documents)} input documents")
        
        # Use RAG to get relevant ADD creation knowledge
        query = "How to create a comprehensive Architecture Design Document (ADD)?"
        rag_result = self.rag_service.query(query, agent_type="SAA")
        
        # In a real implementation, this would use an LLM with the RAG context
        # to generate the actual document content
        
        # For demo purposes, we'll create a placeholder
        add_content = "Architecture Design Document (ADD)\n\n"
        add_content += f"Created using input from: {', '.join(input_documents.keys())}\n\n"
        add_content += f"RAG Context: Used {len(rag_result.retrieved_documents)} relevant architecture references\n\n"
        
        # Add sections from other architecture documents
        for doc_name, doc_content in input_documents.items():
            add_content += f"=== From {doc_name} ===\n\n"
            add_content += f"{doc_content[:200]}...\n\n"  # Truncated for brevity
        
        # Store the created ADD
        self.created_documents["ADD"] = add_content
        
        return {
            "status": "success",
            "document_type": "ADD",
            "document": add_content
        }
