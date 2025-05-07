import os
import json
import logging
from typing import List, Dict, Any, Optional

from src.agents.base_agent import BaseAgent
from src.services.rag_service import RagService
from src.models.base_models import AgentTask, AgentQuery, AgentResponse
from src.utils.logger import setup_logger

logger = setup_logger(__name__, "requirements_agent.log")

class RequirementsAnalysisAgent(BaseAgent):
    """Requirements Analysis Agent (RAA) enhanced with RAG capabilities."""
    
    def __init__(self, agent_id: str = "RAA", name: str = "Requirements Analysis Agent", 
                 max_tokens: int = 4000):
        super().__init__(agent_id, name, max_tokens)
        
        # Initialize RAG service
        self.rag_service = RagService()
        
        # Knowledge areas specific to requirements analysis
        self.knowledge_areas = [
            "requirements engineering",
            "functional requirements",
            "non-functional requirements",
            "user stories",
            "use cases",
            "domain modeling",
            "requirements prioritization",
            "requirements validation",
            "requirements traceability",
            "business rules analysis"
        ]
        
        logger.info(f"Requirements Analysis Agent initialized")
    
    def execute_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Execute a task by its ID with RAG assistance."""
        if task_id not in self.tasks:
            logger.error(f"Task {task_id} not found for agent {self.agent_id}")
            return None
            
        task = self.tasks[task_id]
        task.status = "in_progress"
        
        logger.info(f"RAA executing task: {task.description}")
        
        result = None
        
        # Handle different task types with RAG assistance
        if task.task_type == "analyze_requirements":
            documents = task.input_data.get("documents", {})
            
            # Use RAG to help with requirements analysis
            result = self._analyze_requirements(documents)
            
        elif task.task_type == "extract_functional_requirements":
            document_content = task.input_data.get("document_content", "")
            
            # Use RAG to help with extracting functional requirements
            result = self._extract_functional_requirements(document_content)
            
        elif task.task_type == "extract_non_functional_requirements":
            document_content = task.input_data.get("document_content", "")
            
            # Use RAG to help with extracting non-functional requirements
            result = self._extract_non_functional_requirements(document_content)
            
        elif task.task_type == "create_requirements_report":
            input_data = task.input_data.get("input_data", {})
            
            # Use RAG to help with creating requirements report
            result = self._create_requirements_report(input_data)
        
        # Update task with result
        if result:
            task.status = "completed"
            task.result = result
        else:
            task.status = "failed"
            task.result = {"error": f"Unknown task type or failed execution: {task.task_type}"}
        
        logger.info(f"RAA completed task {task_id} with status {task.status}")
        return task.result
    
    def process_query(self, query: AgentQuery) -> AgentResponse:
        """Process a query from another agent using RAG for enhanced responses."""
        logger.info(f"RAA processing query from {query.sender}: {query.content[:50]}...")
        
        # Use RAG to get relevant requirements knowledge for better response
        rag_result = self.rag_service.query(query.content, agent_type="RAA")
        
        # Extract relevant documents and create sources list
        sources = [
            {
                "content": doc.content[:200] + "...",  # Truncate for brevity
                "source": doc.metadata.get("source", "unknown")
            } for doc in rag_result.retrieved_documents[:3]  # Top 3 most relevant
        ]
        
        # Create response with RAG-enhanced knowledge
        response_content = f"Based on requirements analysis best practices, here's my response:\n\n{rag_result.answer}"
        
        response = AgentResponse(
            query_id=query.query_id,
            sender=self.agent_id,
            recipient=query.sender,
            content=response_content,
            sources=sources
        )
        
        return response
    
    def _analyze_requirements(self, documents: Dict[str, str]) -> Dict[str, Any]:
        """Analyze requirements from project documents with RAG assistance."""
        logger.info(f"Analyzing requirements from {len(documents)} documents")
        
        functional_reqs = []
        non_functional_reqs = []
        data_model_entities = []
        
        for doc_name, doc_content in documents.items():
            # Use RAG to identify requirements in each document
            query = f"Extract key requirements from this document: {doc_name}"
            rag_result = self.rag_service.query(query, agent_type="RAA")
            
            # In a real implementation, this would use an LLM with the RAG context
            # to actually extract and categorize requirements
            
            # For demo purposes, add some placeholder requirements
            if "RR" in doc_name or "requirement" in doc_name.lower():
                functional_reqs.append({
                    "id": f"FR-{len(functional_reqs) + 1}",
                    "description": f"The system shall [requirement from {doc_name}]",
                    "priority": "high",
                    "source": doc_name
                })
                
                non_functional_reqs.append({
                    "id": f"NFR-{len(non_functional_reqs) + 1}",
                    "type": "performance",
                    "description": f"The system shall [performance requirement from {doc_name}]",
                    "measure": "response time < 500ms",
                    "source": doc_name
                })
                
                data_model_entities.append({
                    "name": f"Entity{len(data_model_entities) + 1}",
                    "attributes": ["id", "name", "status"],
                    "relationships": ["relatedTo Entity2"]
                })
        
        # Create final report using RAG-enhanced knowledge
        query = "How to structure a requirements analysis report"
        rag_result = self.rag_service.query(query, agent_type="RAA")
        
        # Placeholder report
        report = {
            "title": "Requirements Analysis Report (RR)",
            "summary": f"Analysis of {len(documents)} documents with RAG assistance",
            "functional_requirements": functional_reqs,
            "non_functional_requirements": non_functional_reqs,
            "data_model": {
                "entities": data_model_entities,
                "relationships": []
            },
            "api_requirements": [],
            "user_roles": [],
            "rag_context": f"Used {len(rag_result.retrieved_documents)} relevant knowledge sources"
        }
        
        return {
            "status": "success",
            "document_type": "RR",
            "document": report
        }
    
    def _extract_functional_requirements(self, document_content: str) -> Dict[str, Any]:
        """Extract functional requirements from document content with RAG assistance."""
        # Use RAG to extract functional requirements
        query = "How to identify and extract functional requirements from project documentation"
        rag_result = self.rag_service.query(query, agent_type="RAA")
        
        # In a real implementation, this would use an LLM with the RAG context
        # to extract the actual requirements
        
        # For demo purposes, we'll create placeholder requirements
        requirements = [
            {
                "id": "FR-1",
                "description": "The system shall provide user authentication",
                "priority": "high"
            },
            {
                "id": "FR-2",
                "description": "The system shall allow document upload",
                "priority": "high"
            },
            {
                "id": "FR-3",
                "description": "The system shall process documents using OCR",
                "priority": "medium"
            }
        ]
        
        return {
            "status": "success",
            "requirements": requirements,
            "count": len(requirements),
            "rag_context": f"Used {len(rag_result.retrieved_documents)} relevant knowledge sources"
        }
    
    def _extract_non_functional_requirements(self, document_content: str) -> Dict[str, Any]:
        """Extract non-functional requirements from document content with RAG assistance."""
        # Use RAG to extract non-functional requirements
        query = "How to identify and extract non-functional requirements from project documentation"
        rag_result = self.rag_service.query(query, agent_type="RAA")
        
        # In a real implementation, this would use an LLM with the RAG context
        # to extract the actual requirements
        
        # For demo purposes, we'll create placeholder requirements
        requirements = [
            {
                "id": "NFR-1",
                "type": "performance",
                "description": "The system shall process documents within 2 seconds",
                "measure": "response time < 2s"
            },
            {
                "id": "NFR-2",
                "type": "security",
                "description": "The system shall encrypt all stored data",
                "measure": "AES-256 encryption"
            },
            {
                "id": "NFR-3",
                "type": "usability",
                "description": "The system shall be accessible to users with visual impairments",
                "measure": "WCAG 2.1 AA compliance"
            }
        ]
        
        return {
            "status": "success",
            "requirements": requirements,
            "count": len(requirements),
            "rag_context": f"Used {len(rag_result.retrieved_documents)} relevant knowledge sources"
        }
    
    def _create_requirements_report(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive requirements report with RAG assistance."""
        # Use RAG to get knowledge about requirements report structure
        query = "How to structure a comprehensive requirements report"
        rag_result = self.rag_service.query(query, agent_type="RAA")
        
        # In a real implementation, this would use an LLM with the RAG context
        # to generate the actual report content
        
        functional_reqs = input_data.get("functional_requirements", [])
        non_functional_reqs = input_data.get("non_functional_requirements", [])
        
        # For demo purposes, create a placeholder report
        report = {
            "title": "Requirements Analysis Report (RR)",
            "date": "2025-05-06",
            "version": "1.0",
            "summary": f"This report contains {len(functional_reqs)} functional requirements and {len(non_functional_reqs)} non-functional requirements",
            "sections": [
                {
                    "title": "Introduction",
                    "content": "This document outlines the requirements for the system..."
                },
                {
                    "title": "Functional Requirements",
                    "requirements": functional_reqs
                },
                {
                    "title": "Non-Functional Requirements",
                    "requirements": non_functional_reqs
                },
                {
                    "title": "Data Model",
                    "content": "The system will manage the following data entities..."
                },
                {
                    "title": "User Roles and Permissions",
                    "content": "The system will support the following user roles..."
                }
            ],
            "rag_context": f"Used {len(rag_result.retrieved_documents)} relevant knowledge sources"
        }
        
        return {
            "status": "success",
            "document_type": "RR",
            "document": report
        }
