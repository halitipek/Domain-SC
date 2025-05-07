"""
Technology Analysis Agent (TAA) implementation
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional

from src.agents.base_agent import BaseAgent
from src.services.rag_service import RagService
from src.models.base_models import AgentTask, AgentQuery, AgentResponse
from src.utils.logger import setup_logger
from src.prompts.prompt_manager import PromptManager

logger = setup_logger(__name__, "technology_agent.log")

class TechnologyAnalysisAgent(BaseAgent):
    """Technology Analysis Agent (TAA) for analyzing technical requirements and recommending technologies."""
    
    def __init__(self, agent_id: str = "TAA", name: str = "Technology Analysis Agent", 
                 max_tokens: int = 4000):
        super().__init__(agent_id, name, max_tokens)
        
        # Initialize RAG service for technical knowledge
        self.rag_service = RagService()
        
        # Initialize prompt manager
        self.prompt_manager = PromptManager()
        
        # Knowledge areas for the TAA
        self.knowledge_areas = [
            "software frameworks",
            "programming languages",
            "databases",
            "cloud services",
            "infrastructure technologies",
            "security technologies",
            "integration patterns",
            "performance optimization",
            "scalability solutions",
            "dev tools and libraries"
        ]
        
        # Track created documents
        self.created_documents = {
            "TR": None,  # Technology Report
            "TR-SUM": None,  # Technology Report Summary
        }
        
        logger.info(f"Technology Analysis Agent initialized")
    
    def execute_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Execute a task by its ID with RAG assistance."""
        if task_id not in self.tasks:
            logger.error(f"Task {task_id} not found for agent {self.agent_id}")
            return None
            
        task = self.tasks[task_id]
        task.status = "in_progress"
        
        logger.info(f"TAA executing task: {task.description}")
        
        result = None
        
        # Handle different task types with RAG assistance
        if task.task_type == "analyze_technology":
            documents = task.input_data.get("documents", {})
            
            # Use RAG to help with technology analysis
            result = self._analyze_technology(documents)
            
        elif task.task_type == "analyze_ocr_requirements":
            requirements = task.input_data.get("requirements", "")
            
            # Use RAG to help with OCR analysis
            result = self._analyze_ocr_requirements(requirements)
            
        elif task.task_type == "analyze_rag_requirements":
            requirements = task.input_data.get("requirements", "")
            
            # Use RAG to help with RAG analysis
            result = self._analyze_rag_requirements(requirements)
            
        elif task.task_type == "evaluate_technology_stack":
            tech_stack = task.input_data.get("technology_stack", {})
            requirements = task.input_data.get("requirements", {})
            constraints = task.input_data.get("constraints", {})
            
            # Use RAG to help with technology stack evaluation
            result = self._evaluate_technology_stack(tech_stack, requirements, constraints)
        
        # Update task with result
        if result:
            task.status = "completed"
            task.result = result
        else:
            task.status = "failed"
            task.result = {"error": f"Unknown task type or failed execution: {task.task_type}"}
        
        logger.info(f"TAA completed task {task_id} with status {task.status}")
        return task.result
    
    def process_query(self, query: AgentQuery) -> AgentResponse:
        """Process a query from another agent using RAG for enhanced responses."""
        logger.info(f"TAA processing query from {query.sender}: {query.content[:50]}...")
        
        # Get prompt for query processing
        prompt = self.prompt_manager.get_prompt(
            agent_id=self.agent_id, 
            prompt_type="query_processing",
            query=query.content
        )
        
        # Use RAG to get relevant technical knowledge
        rag_result = self.rag_service.query(query.content, agent_type="TAA")
        
        # Extract relevant documents and create sources list
        sources = [
            {
                "content": doc.content[:200] + "...",  # Truncate for brevity
                "source": doc.metadata.get("source", "unknown")
            } for doc in rag_result.retrieved_documents[:3]  # Top 3 most relevant
        ]
        
        # Use knowledge from RAG to enhance the response
        # In a real implementation, this would use an LLM with the prompt and RAG context
        response_content = f"Based on technology analysis, here's my response:\n\n{rag_result.answer}"
        
        response = AgentResponse(
            query_id=query.query_id,
            sender=self.agent_id,
            recipient=query.sender,
            content=response_content,
            sources=sources
        )
        
        return response
    
    def _analyze_technology(self, documents: Dict[str, str]) -> Dict[str, Any]:
        """Analyze technology requirements and recommend solutions with RAG assistance."""
        logger.info(f"Analyzing technology requirements from {len(documents)} documents")
        
        # Get documents description
        documents_description = "\n".join([f"- {name}: {content[:300]}..." for name, content in documents.items()])
        
        # Get prompt for technology analysis
        prompt = self.prompt_manager.get_prompt(
            agent_id=self.agent_id, 
            prompt_type="analyze_technology",
            documents_description=documents_description
        )
        
        # Use RAG to get relevant technical knowledge
        query = "Best practices for technology stack selection and technology analysis"
        rag_result = self.rag_service.query(query, agent_type="TAA")
        
        # In a real implementation, this would use an LLM with the prompt and RAG context
        # to generate the actual analysis
        
        # For demo purposes, create a placeholder report
        technical_requirements = []
        technology_recommendations = []
        technology_stack = {
            "backend": ["Python", "Django/Flask"],
            "frontend": ["React", "TypeScript"],
            "database": ["PostgreSQL"],
            "infrastructure": ["Docker", "Kubernetes"],
            "security": ["OAuth 2.0", "HTTPS/TLS"],
            "integration": ["REST APIs", "GraphQL"]
        }
        technical_risks = []
        
        # Extract some requirements from documents
        for doc_name, doc_content in documents.items():
            # This would normally use an LLM to extract requirements
            if "requirement" in doc_name.lower() or "RR" in doc_name or "TR" in doc_name:
                technical_requirements.append({
                    "id": f"TR-{len(technical_requirements) + 1}",
                    "category": "integration" if "integration" in doc_content.lower() else "infrastructure",
                    "description": f"The system should support [extracted from {doc_name}]",
                    "criticality": "high",
                    "source": doc_name
                })
                
                technology_recommendations.append({
                    "category": "database",
                    "recommended_technology": "PostgreSQL",
                    "version": "14.x",
                    "rationale": "Provides robust ACID compliance, excellent performance, and has strong community support",
                    "alternatives": ["MySQL", "MongoDB"],
                    "satisfied_requirements": [f"TR-{len(technical_requirements)}"]
                })
                
                technical_risks.append({
                    "id": f"RISK-{len(technical_risks) + 1}",
                    "description": f"Risk related to [extracted from {doc_name}]",
                    "impact": "medium",
                    "mitigation": "Implement X to mitigate this risk"
                })
        
        # Create report
        report = {
            "title": "Technology Analysis Report (TR)",
            "summary": f"Analysis of {len(documents)} documents with RAG assistance, identifying {len(technical_requirements)} technical requirements",
            "technical_requirements": technical_requirements,
            "technology_recommendations": technology_recommendations,
            "technology_stack": technology_stack,
            "technical_risks": technical_risks,
            "implementation_considerations": [
                "Consider containerization for consistent deployment",
                "Implement CI/CD pipelines for automated testing and deployment"
            ]
        }
        
        # Store the report
        self.created_documents["TR"] = report
        
        # Create summary (TR-SUM)
        summary = {
            "title": "Technology Analysis Report Summary (TR-SUM)",
            "key_technologies": technology_stack,
            "requirement_count": len(technical_requirements),
            "recommendation_count": len(technology_recommendations),
            "risk_count": len(technical_risks)
        }
        
        self.created_documents["TR-SUM"] = summary
        
        return {
            "status": "success",
            "document_type": "TR",
            "document": report
        }
    
    def _analyze_ocr_requirements(self, requirements: str) -> Dict[str, Any]:
        """Analyze OCR requirements and recommend solutions with RAG assistance."""
        logger.info(f"Analyzing OCR requirements")
        
        # Get prompt for OCR analysis
        prompt = self.prompt_manager.get_prompt(
            agent_id=self.agent_id, 
            prompt_type="analyze_ocr_requirements",
            requirements_description=requirements[:1000]  # Limit length
        )
        
        # Use RAG to get relevant OCR knowledge
        query = "OCR technologies and document processing solutions"
        rag_result = self.rag_service.query(query, agent_type="TAA")
        
        # In a real implementation, this would use an LLM with the prompt and RAG context
        
        # For demo purposes, create a placeholder analysis
        ocr_requirements = [
            {
                "id": "OCR-001",
                "description": "The system must extract text from scanned PDF documents",
                "document_types": ["PDF", "Scanned documents"],
                "priority": "high"
            },
            {
                "id": "OCR-002",
                "description": "The system must recognize tables in documents",
                "document_types": ["PDF", "Images"],
                "priority": "medium"
            }
        ]
        
        recommended_solutions = [
            {
                "name": "Tesseract OCR",
                "type": "open-source",
                "capabilities": ["Text extraction", "Layout analysis", "Multiple language support"],
                "use_case": "Basic OCR for text extraction",
                "rationale": "Well-established, mature OCR engine with good accuracy for clean documents",
                "integration_approach": "Use as a Python library via pytesseract"
            },
            {
                "name": "AWS Textract",
                "type": "commercial",
                "capabilities": ["Text extraction", "Form extraction", "Table extraction"],
                "use_case": "Advanced document processing with table recognition",
                "rationale": "High accuracy for complex documents with tables and forms",
                "integration_approach": "API integration through AWS SDK"
            }
        ]
        
        analysis = {
            "ocr_requirements": ocr_requirements,
            "recommended_solutions": recommended_solutions,
            "implementation_considerations": [
                "Implement pre-processing to improve document quality before OCR",
                "Consider a hybrid approach for different document types"
            ],
            "expected_accuracy": "90-95% for clean documents, 75-85% for complex layouts",
            "performance_estimates": "1-5 seconds per page depending on complexity"
        }
        
        return {
            "status": "success",
            "analysis": analysis
        }
    
    def _analyze_rag_requirements(self, requirements: str) -> Dict[str, Any]:
        """Analyze RAG requirements and recommend solutions with RAG assistance."""
        logger.info(f"Analyzing RAG requirements")
        
        # Get prompt for RAG analysis
        prompt = self.prompt_manager.get_prompt(
            agent_id=self.agent_id, 
            prompt_type="analyze_rag_requirements",
            requirements_description=requirements[:1000]  # Limit length
        )
        
        # Use RAG to get relevant RAG knowledge
        query = "Retrieval Augmented Generation technologies and implementation approaches"
        rag_result = self.rag_service.query(query, agent_type="TAA")
        
        # In a real implementation, this would use an LLM with the prompt and RAG context
        
        # For demo purposes, create a placeholder analysis
        rag_requirements = [
            {
                "id": "RAG-001",
                "description": "The system must retrieve relevant architectural knowledge to assist the SAA",
                "knowledge_domain": "System architecture",
                "priority": "high"
            },
            {
                "id": "RAG-002",
                "description": "The system must maintain context across multiple queries",
                "knowledge_domain": "All domains",
                "priority": "medium"
            }
        ]
        
        recommended_components = {
            "vector_database": {
                "name": "ChromaDB",
                "rationale": "Lightweight, easy to integrate, and supports document metadata",
                "alternatives": ["Pinecone", "Weaviate", "Milvus"]
            },
            "embedding_model": {
                "name": "sentence-transformers/all-MiniLM-L6-v2",
                "rationale": "Good balance of performance and resource usage",
                "alternatives": ["OpenAI Embeddings", "BERT-based models"]
            },
            "chunking_strategy": "Recursive character text splitting with 500-token chunks and 50-token overlap",
            "retrieval_mechanism": "Similarity search with top-k=5 results",
            "llm_integration": "Pass retrieved context in system message with clear instructions"
        }
        
        analysis = {
            "rag_requirements": rag_requirements,
            "recommended_components": recommended_components,
            "implementation_architecture": "Hybrid retrieval system with specialized retrievers for different knowledge domains",
            "performance_considerations": [
                "Cache frequent queries to reduce latency",
                "Implement batched embedding generation for efficiency"
            ],
            "scalability_approach": "Shard vector database as knowledge base grows",
            "estimated_resource_requirements": "2-4GB RAM for embedding models, 10-20GB storage for vector database"
        }
        
        return {
            "status": "success",
            "analysis": analysis
        }
    
    def _evaluate_technology_stack(self, tech_stack: Dict, requirements: Dict, constraints: Dict) -> Dict[str, Any]:
        """Evaluate a technology stack with RAG assistance."""
        logger.info(f"Evaluating technology stack")
        
        # Format descriptions for the prompt
        tech_stack_desc = json.dumps(tech_stack, indent=2)[:1000]
        requirements_desc = json.dumps(requirements, indent=2)[:1000]
        constraints_desc = json.dumps(constraints, indent=2)[:1000]
        
        # Get prompt for technology stack evaluation
        prompt = self.prompt_manager.get_prompt(
            agent_id=self.agent_id, 
            prompt_type="evaluate_technology_stack",
            technology_stack_description=tech_stack_desc,
            requirements_description=requirements_desc,
            constraints_description=constraints_desc
        )
        
        # Use RAG to get relevant knowledge
        query = "Technology stack evaluation criteria and best practices"
        rag_result = self.rag_service.query(query, agent_type="TAA")
        
        # In a real implementation, this would use an LLM with the prompt and RAG context
        
        # For demo purposes, create a placeholder evaluation
        component_evaluations = []
        for component, details in tech_stack.items():
            component_evaluations.append({
                "component": component,
                "category": "backend" if component in ["Python", "Django", "Flask"] else 
                            "frontend" if component in ["React", "Angular", "Vue"] else 
                            "database" if component in ["PostgreSQL", "MongoDB", "MySQL"] else 
                            "infrastructure",
                "rating": "Strong",
                "strengths": ["Well-established", "Strong community support"],
                "concerns": ["Learning curve"] if component in ["Kubernetes", "GraphQL"] else [],
                "alternatives": ["Alternative technologies"]
            })
        
        evaluation = {
            "overall_assessment": "The proposed technology stack is well-aligned with the system requirements",
            "component_evaluations": component_evaluations,
            "integration_assessment": {
                "compatibility": "Components are generally compatible with established integration patterns",
                "concerns": ["Some potential version compatibility issues between X and Y"],
                "recommendations": ["Use Docker to ensure consistent environments"]
            },
            "performance_assessment": "The stack should meet performance requirements with proper implementation",
            "scalability_assessment": "Good support for horizontal scaling with Kubernetes",
            "security_assessment": "Strong security capabilities, but requires proper configuration",
            "maintainability_assessment": "Good maintainability with modern frameworks and tools",
            "recommendations": [
                "Consider adding automated testing frameworks",
                "Implement CI/CD pipelines from the start"
            ]
        }
        
        return {
            "status": "success",
            "evaluation": evaluation
        }