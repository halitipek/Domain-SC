"""
Optimization Analysis Agent (OAA) implementation
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

logger = setup_logger(__name__, "optimization_agent.log")

class OptimizationAnalysisAgent(BaseAgent):
    """Optimization Analysis Agent (OAA) for performance and resource optimization."""
    
    def __init__(self, agent_id: str = "OAA", name: str = "Optimization Analysis Agent", 
                 max_tokens: int = 4000):
        super().__init__(agent_id, name, max_tokens)
        
        # Initialize RAG service for optimization knowledge
        self.rag_service = RagService()
        
        # Initialize prompt manager
        self.prompt_manager = PromptManager()
        
        # Knowledge areas for the OAA
        self.knowledge_areas = [
            "performance optimization",
            "resource utilization",
            "scalability planning",
            "cost optimization",
            "efficiency improvements",
            "bottleneck analysis",
            "capacity planning",
            "load testing",
            "caching strategies",
            "database optimization"
        ]
        
        # Track created documents
        self.created_documents = {
            "OR": None,  # Optimization Report
            "OR-SUM": None,  # Optimization Report Summary
        }
        
        logger.info(f"Optimization Analysis Agent initialized")
    
    def execute_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Execute a task by its ID with RAG assistance."""
        if task_id not in self.tasks:
            logger.error(f"Task {task_id} not found for agent {self.agent_id}")
            return None
            
        task = self.tasks[task_id]
        task.status = "in_progress"
        
        logger.info(f"OAA executing task: {task.description}")
        
        result = None
        
        # Handle different task types with RAG assistance
        if task.task_type == "analyze_optimization":
            documents = task.input_data.get("documents", {})
            
            # Use RAG to help with optimization analysis
            result = self._analyze_optimization(documents)
            
        elif task.task_type == "analyze_llm_optimization":
            llm_usage = task.input_data.get("llm_usage", "")
            
            # Use RAG to help with LLM optimization analysis
            result = self._analyze_llm_optimization(llm_usage)
            
        elif task.task_type == "develop_scalability_strategy":
            requirements = task.input_data.get("requirements", "")
            
            # Use RAG to help with scalability strategy
            result = self._develop_scalability_strategy(requirements)
            
        elif task.task_type == "cost_optimization_analysis":
            resource_usage = task.input_data.get("resource_usage", "")
            
            # Use RAG to help with cost optimization
            result = self._cost_optimization_analysis(resource_usage)
        
        # Update task with result
        if result:
            task.status = "completed"
            task.result = result
        else:
            task.status = "failed"
            task.result = {"error": f"Unknown task type or failed execution: {task.task_type}"}
        
        logger.info(f"OAA completed task {task_id} with status {task.status}")
        return task.result
    
    def process_query(self, query: AgentQuery) -> AgentResponse:
        """Process a query from another agent using RAG for enhanced responses."""
        logger.info(f"OAA processing query from {query.sender}: {query.content[:50]}...")
        
        # Get prompt for query processing
        prompt = self.prompt_manager.get_prompt(
            agent_id=self.agent_id, 
            prompt_type="query_processing",
            query=query.content
        )
        
        # Use RAG to get relevant optimization knowledge
        rag_result = self.rag_service.query(query.content, agent_type="OAA")
        
        # Extract relevant documents and create sources list
        sources = [
            {
                "content": doc.content[:200] + "...",  # Truncate for brevity
                "source": doc.metadata.get("source", "unknown")
            } for doc in rag_result.retrieved_documents[:3]  # Top 3 most relevant
        ]
        
        # Use knowledge from RAG to enhance the response
        # In a real implementation, this would use an LLM with the prompt and RAG context
        response_content = f"Based on optimization analysis, here's my response:\n\n{rag_result.answer}"
        
        response = AgentResponse(
            query_id=query.query_id,
            sender=self.agent_id,
            recipient=query.sender,
            content=response_content,
            sources=sources
        )
        
        return response
    
    def _analyze_optimization(self, documents: Dict[str, str]) -> Dict[str, Any]:
        """Analyze optimization opportunities and develop strategies with RAG assistance."""
        logger.info(f"Analyzing optimization opportunities from {len(documents)} documents")
        
        # Get documents description
        documents_description = "\n".join([f"- {name}: {content[:300]}..." for name, content in documents.items()])
        
        # Get prompt for optimization analysis
        prompt = self.prompt_manager.get_prompt(
            agent_id=self.agent_id, 
            prompt_type="analyze_optimization",
            documents_description=documents_description
        )
        
        # Use RAG to get relevant optimization knowledge
        query = "Best practices for performance optimization and efficiency improvements"
        rag_result = self.rag_service.query(query, agent_type="OAA")
        
        # In a real implementation, this would use an LLM with the prompt and RAG context
        # to generate the actual analysis
        
        # For demo purposes, create a placeholder report
        performance_requirements = []
        system_constraints = []
        optimization_strategies = []
        llm_optimization = {
            "prompt_optimization": [
                "Use clear and concise prompts",
                "Include specific instructions at the beginning"
            ],
            "context_management": [
                "Minimize context size by using relevant information only",
                "Implement context pruning for long conversations"
            ],
            "caching_strategies": [
                "Cache frequent queries",
                "Implement result caching with appropriate TTL"
            ],
            "batching_approaches": [
                "Batch similar requests",
                "Implement async processing for batched requests"
            ],
            "model_selection": [
                "Use smaller models for simpler tasks",
                "Reserve advanced models for complex reasoning"
            ]
        }
        
        # Extract some requirements from documents
        for doc_name, doc_content in documents.items():
            # This would normally use an LLM to extract requirements
            if "performance" in doc_name.lower() or "requirement" in doc_name.lower():
                performance_requirements.append({
                    "id": f"PR-{len(performance_requirements) + 1}",
                    "category": "response time" if "response" in doc_content.lower() else "throughput",
                    "description": f"The system should [performance requirement from {doc_name}]",
                    "target_metric": "< 500ms response time",
                    "criticality": "high",
                    "source": doc_name
                })
                
                system_constraints.append({
                    "id": f"SC-{len(system_constraints) + 1}",
                    "category": "hardware" if "hardware" in doc_content.lower() else "budget",
                    "description": f"[Constraint from {doc_name}]",
                    "impact": "Limits horizontal scaling options",
                    "source": doc_name
                })
                
                optimization_strategies.append({
                    "id": f"OS-{len(optimization_strategies) + 1}",
                    "title": f"Optimization strategy for {doc_name}",
                    "description": "Detailed description of the optimization strategy",
                    "target_areas": ["Component 1", "Component 2"],
                    "expected_benefits": "20-30% improvement in response time",
                    "implementation_complexity": "medium",
                    "priority": "high",
                    "trade_offs": "Increased memory usage",
                    "measurement_approach": "Before/after performance testing"
                })
        
        # Create report
        report = {
            "title": "Optimization Analysis Report (OR)",
            "summary": f"Analysis of {len(documents)} documents with RAG assistance, identifying {len(performance_requirements)} performance requirements",
            "performance_requirements": performance_requirements,
            "system_constraints": system_constraints,
            "optimization_strategies": optimization_strategies,
            "llm_optimization": llm_optimization,
            "cost_optimization": {
                "estimated_costs": "Estimated monthly cost: $X",
                "cost_reduction_strategies": [
                    "Implement auto-scaling to reduce idle resources",
                    "Use spot instances for non-critical workloads"
                ],
                "roi_analysis": "Expected ROI: X% over Y months"
            },
            "implementation_roadmap": {
                "phases": [
                    {
                        "phase": "Phase 1: Quick Wins",
                        "strategies": ["OS-1"],
                        "estimated_effort": "2-3 developer weeks",
                        "expected_outcomes": "15-20% performance improvement"
                    }
                ]
            }
        }
        
        # Store the report
        self.created_documents["OR"] = report
        
        # Create summary (OR-SUM)
        summary = {
            "title": "Optimization Analysis Report Summary (OR-SUM)",
            "key_strategies": [s["title"] for s in optimization_strategies],
            "requirement_count": len(performance_requirements),
            "constraint_count": len(system_constraints),
            "strategy_count": len(optimization_strategies)
        }
        
        self.created_documents["OR-SUM"] = summary
        
        return {
            "status": "success",
            "document_type": "OR",
            "document": report
        }
    
    def _analyze_llm_optimization(self, llm_usage: str) -> Dict[str, Any]:
        """Analyze LLM usage and develop optimization strategies with RAG assistance."""
        logger.info(f"Analyzing LLM optimization opportunities")
        
        # Get prompt for LLM optimization analysis
        prompt = self.prompt_manager.get_prompt(
            agent_id=self.agent_id, 
            prompt_type="analyze_llm_optimization",
            llm_usage_description=llm_usage[:1000]  # Limit length
        )
        
        # Use RAG to get relevant LLM optimization knowledge
        query = "LLM optimization strategies and best practices"
        rag_result = self.rag_service.query(query, agent_type="OAA")
        
        # In a real implementation, this would use an LLM with the prompt and RAG context
        
        # For demo purposes, create a placeholder analysis
        current_usage_patterns = {
            "typical_prompts": ["Long context with detailed instructions", "Multi-turn conversation context"],
            "context_size": "Average 2000-4000 tokens per request",
            "request_frequency": "50-100 requests per hour during peak usage",
            "models_used": ["gpt-4-1106-preview", "gpt-3.5-turbo"]
        }
        
        optimization_strategies = [
            {
                "id": "LLMO-001",
                "category": "prompt",
                "title": "Prompt Template Optimization",
                "description": "Redesign prompt templates to be more concise and specific",
                "expected_benefits": "20-30% reduction in prompt tokens, improved response quality",
                "implementation_approach": "Create standardized prompt templates with clear sections",
                "priority": "high"
            },
            {
                "id": "LLMO-002",
                "category": "caching",
                "title": "Response Caching",
                "description": "Implement caching for common queries with similar contexts",
                "expected_benefits": "40-50% reduction in API calls for frequently asked questions",
                "implementation_approach": "Use vector similarity to identify semantically similar queries",
                "priority": "high"
            }
        ]
        
        analysis = {
            "current_usage_patterns": current_usage_patterns,
            "optimization_strategies": optimization_strategies,
            "prompt_engineering_recommendations": [
                "Use numbered lists for multi-step instructions",
                "Place critical instructions at the beginning and end of prompts"
            ],
            "context_optimization": [
                "Implement context pruning for long conversations",
                "Use token counting to prevent context overflow"
            ],
            "caching_strategy": {
                "cacheable_content": ["Factual information", "Static responses", "Frequently asked questions"],
                "cache_invalidation": "Time-based TTL with selective purging",
                "implementation_approach": "Use Redis with vector similarity checking"
            },
            "model_selection_guidance": [
                {
                    "task": "Simple classification",
                    "recommended_model": "gpt-3.5-turbo",
                    "rationale": "High performance at lower cost for simpler tasks"
                },
                {
                    "task": "Complex reasoning",
                    "recommended_model": "gpt-4-turbo",
                    "rationale": "Superior reasoning capabilities for complex tasks justify higher cost"
                }
            ],
            "cost_projections": {
                "current_estimated_cost": "$5000 per month",
                "optimized_estimated_cost": "$2500-3000 per month",
                "percentage_reduction": "40-50%"
            },
            "implementation_roadmap": "Phase 1: Prompt optimization and caching (2 weeks)\nPhase 2: Model selection optimization (1 week)\nPhase 3: Context management (2 weeks)"
        }
        
        return {
            "status": "success",
            "analysis": analysis
        }
    
    def _develop_scalability_strategy(self, requirements: str) -> Dict[str, Any]:
        """Develop a scalability strategy with RAG assistance."""
        logger.info(f"Developing scalability strategy")
        
        # Get prompt for scalability strategy
        prompt = self.prompt_manager.get_prompt(
            agent_id=self.agent_id, 
            prompt_type="develop_scalability_strategy",
            requirements_description=requirements[:1000]  # Limit length
        )
        
        # Use RAG to get relevant scalability knowledge
        query = "Scalability strategies and best practices for high-growth systems"
        rag_result = self.rag_service.query(query, agent_type="OAA")
        
        # In a real implementation, this would use an LLM with the prompt and RAG context
        
        # For demo purposes, create a placeholder strategy
        growth_projections = {
            "current_load": "1000 concurrent users, 100 requests/second",
            "projected_growth": "50% growth every 6 months for the next 2 years",
            "key_metrics": ["Concurrent users", "Requests per second", "Data storage growth", "Response time"]
        }
        
        scalability_challenges = [
            {
                "component": "Database",
                "challenge": "Growing dataset with complex queries",
                "impact": "Increasing query times and resource consumption",
                "criticality": "high"
            },
            {
                "component": "API Services",
                "challenge": "Increasing request volume",
                "impact": "Higher latency during peak hours",
                "criticality": "high"
            }
        ]
        
        scaling_strategies = [
            {
                "id": "SS-001",
                "component": "Database",
                "approach": "horizontal",
                "description": "Implement database sharding by customer ID",
                "implementation": "Use PostgreSQL with application-level sharding",
                "triggers": "When query response time exceeds 100ms or database CPU > 70%",
                "limitations": "Complexity in cross-shard queries"
            },
            {
                "id": "SS-002",
                "component": "API Services",
                "approach": "horizontal",
                "description": "Deploy API services in auto-scaling groups",
                "implementation": "Use Kubernetes with HPA based on CPU and request metrics",
                "triggers": "When CPU > 60% or request queue length > 100",
                "limitations": "Cold start latency for new instances"
            }
        ]
        
        strategy = {
            "summary": "A comprehensive scalability strategy focusing on horizontal scaling of key components",
            "growth_projections": growth_projections,
            "scalability_challenges": scalability_challenges,
            "scaling_strategies": scaling_strategies,
            "database_scaling": {
                "current_architecture": "Single PostgreSQL instance",
                "scaling_approach": "Horizontal sharding with read replicas",
                "sharding_strategy": "Shard by customer ID with consistent hashing",
                "replication_strategy": "One primary with multiple read replicas per shard",
                "migration_path": "Gradual migration using dual-write approach"
            },
            "application_scaling": {
                "stateless_components": "Horizontal scaling with load balancing",
                "stateful_components": "Session data in distributed cache",
                "caching_strategy": "Distributed cache with local in-memory caches"
            },
            "infrastructure_recommendations": {
                "compute": "Auto-scaling instance groups with right-sized instances",
                "storage": "Scalable object storage for files, sharded databases for structured data",
                "networking": "CDN for static content, API gateway with rate limiting",
                "cloud_services": "Managed Kubernetes, managed database services, serverless functions for bursty workloads"
            },
            "cost_projections": {
                "current_costs": "$10,000/month",
                "projected_costs": "$25,000/month after 2 years of growth",
                "optimization_opportunities": "Reserved instances, spot instances for batch processing"
            },
            "implementation_roadmap": "Phase 1: Monitoring and baseline (1 month)\nPhase 2: Application scaling (2 months)\nPhase 3: Database scaling (3 months)"
        }
        
        return {
            "status": "success",
            "strategy": strategy
        }
    
    def _cost_optimization_analysis(self, resource_usage: str) -> Dict[str, Any]:
        """Analyze resource usage and develop cost optimization strategies with RAG assistance."""
        logger.info(f"Analyzing cost optimization opportunities")
        
        # Get prompt for cost optimization
        prompt = self.prompt_manager.get_prompt(
            agent_id=self.agent_id, 
            prompt_type="cost_optimization_analysis",
            resource_usage_description=resource_usage[:1000]  # Limit length
        )
        
        # Use RAG to get relevant cost optimization knowledge
        query = "Cost optimization strategies for cloud infrastructure and software systems"
        rag_result = self.rag_service.query(query, agent_type="OAA")
        
        # In a real implementation, this would use an LLM with the prompt and RAG context
        
        # For demo purposes, create a placeholder analysis
        current_cost_breakdown = {
            "compute": "$5,000/month",
            "storage": "$2,000/month",
            "network": "$1,000/month",
            "services": "$2,000/month",
            "total_monthly": "$10,000/month"
        }
        
        inefficiencies_identified = [
            {
                "area": "Compute resources",
                "description": "Over-provisioned instances running at low utilization",
                "estimated_waste": "$1,500/month",
                "root_cause": "Static provisioning without auto-scaling"
            },
            {
                "area": "Storage",
                "description": "Redundant data storage and unnecessary replication",
                "estimated_waste": "$800/month",
                "root_cause": "Lack of data lifecycle management"
            }
        ]
        
        optimization_strategies = [
            {
                "id": "CO-001",
                "title": "Implement Auto-scaling",
                "category": "infrastructure",
                "description": "Replace static instance groups with auto-scaling groups based on utilization metrics",
                "implementation_approach": "Use Kubernetes HPA or cloud-specific auto-scaling",
                "estimated_savings": "$1,200/month",
                "implementation_cost": "$5,000",
                "roi_timeline": "4-5 months",
                "risks": "Potential cold-start latency, need for proper monitoring",
                "priority": "high"
            },
            {
                "id": "CO-002",
                "title": "Storage Tiering",
                "category": "infrastructure",
                "description": "Implement storage lifecycle policies to move aging data to cheaper storage tiers",
                "implementation_approach": "Use cloud storage lifecycle policies and automation scripts",
                "estimated_savings": "$600/month",
                "implementation_cost": "$3,000",
                "roi_timeline": "5 months",
                "risks": "Increased access latency for older data",
                "priority": "medium"
            }
        ]
        
        analysis = {
            "current_cost_breakdown": current_cost_breakdown,
            "inefficiencies_identified": inefficiencies_identified,
            "optimization_strategies": optimization_strategies,
            "projected_cost_reduction": {
                "monthly_savings": "$2,500/month",
                "percentage_reduction": "25%",
                "annual_impact": "$30,000"
            },
            "implementation_roadmap": "Phase 1: Auto-scaling (1 month)\nPhase 2: Storage optimization (1 month)\nPhase 3: Reserved/Spot instances (2 weeks)",
            "monitoring_recommendations": "Implement detailed cost allocation tags, daily cost monitoring alerts, and monthly optimization reviews"
        }
        
        return {
            "status": "success",
            "analysis": analysis
        }