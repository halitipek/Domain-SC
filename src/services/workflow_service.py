"""
Workflow Service for the Domain-SC system.
This service manages multi-agent workflows and orchestration.
"""

import os
import json
import logging
import asyncio
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime

from src.utils.logger import setup_logger
from src.services.rag_service import RagService
from src.services.llm_service import LLMService
from src.services.agent_registry import AgentRegistry

logger = setup_logger(__name__, "workflow_service.log")

class WorkflowService:
    """Service for managing multi-agent workflows."""
    
    def __init__(self):
        """Initialize the workflow service."""
        # Initialize the agent registry
        self.agent_registry = AgentRegistry()
        
        # Initialize RAG service
        self.rag_service = RagService()
        
        # Initialize LLM service
        self.llm_service = LLMService()
        
        # Initialize core agents
        self.agents = self.agent_registry.initialize_core_agents()
        
        # Get the orchestrator agent
        self.orchestrator = self.agents["OA"]
        
        # Setup event callbacks
        self._setup_callbacks()
        
        # Track workflows
        self.workflows = {}
        
        logger.info("Workflow Service initialized")
    
    def _setup_callbacks(self):
        """Setup callbacks for agent interactions."""
        # Register callbacks for orchestrator events
        self.orchestrator.register_callback("message_sent", self._on_message_sent)
        self.orchestrator.register_callback("task_created", self._on_task_created)
        self.orchestrator.register_callback("task_completed", self._on_task_completed)
    
    def _on_message_sent(self, message):
        """Handle message sent event."""
        recipient = message.recipient
        
        # If recipient agent doesn't exist yet, create it
        if recipient not in self.agents:
            self._create_agent(recipient)
        
        # Deliver the message to the recipient
        if recipient in self.agents:
            self.agents[recipient].receive_message(message)
    
    def _on_task_created(self, task):
        """Handle task created event."""
        logger.info(f"Task created: {task.task_id} for agent {task.agent_id}")
    
    def _on_task_completed(self, task):
        """Handle task completed event."""
        logger.info(f"Task completed: {task.task_id} by agent {task.agent_id}")
    
    def _create_agent(self, agent_id):
        """Create an agent by ID."""
        logger.info(f"Creating agent: {agent_id}")
        
        # Use the agent registry to create the agent
        agent = self.agent_registry.create_agent(agent_id)
        
        if agent:
            self.agents[agent_id] = agent
            
            # Get agent capabilities from registry
            capabilities = self.agent_registry.agent_capabilities.get(agent_id, ["basic_tasks"])
            
            # Register the agent with the orchestrator
            self.orchestrator.register_agent(agent_id, agent_id, capabilities)
        else:
            logger.warning(f"Failed to create agent {agent_id}")
    
    async def initialize_workflow(self, workflow_name: str, input_files: List[str]) -> Dict[str, Any]:
        """Initialize a new workflow.
        
        Args:
            workflow_name: Name of the workflow
            input_files: List of input file paths
            
        Returns:
            Workflow initialization result
        """
        logger.info(f"Initializing workflow: {workflow_name} with {len(input_files)} input files")
        
        # Create a workflow ID
        workflow_id = f"{workflow_name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # 1. Index input files for RAG
        index_result = self.rag_service.index_documents(input_files, collection_name=workflow_id)
        
        # 2. Create and start workflow task for orchestrator
        task = self.orchestrator.create_task(
            description=f"Start workflow: {workflow_name}",
            task_type="start_workflow",
            input_data={
                "workflow_name": workflow_name,
                "input_files": input_files
            }
        )
        
        # 3. Execute the task
        result = self.orchestrator.execute_task(task.task_id)
        
        # 4. Store workflow information
        self.workflows[workflow_id] = {
            "id": workflow_id,
            "name": workflow_name,
            "start_time": datetime.utcnow().isoformat(),
            "status": "active",
            "input_files": input_files,
            "current_phase": "document_discovery",
            "completed_phases": [],
            "tasks": {task.task_id: task.dict()},
            "documents": {}
        }
        
        return {
            "workflow_id": workflow_id,
            "status": "initialized",
            "workflow_name": workflow_name,
            "task_id": task.task_id,
            "rag_index": index_result,
            "result": result
        }
    
    async def advance_workflow(self, workflow_id: str, next_phase: str) -> Dict[str, Any]:
        """Advance the workflow to the next phase.
        
        Args:
            workflow_id: ID of the workflow to advance
            next_phase: The next phase to advance to
            
        Returns:
            Workflow advancement result
        """
        logger.info(f"Advancing workflow {workflow_id} to phase: {next_phase}")
        
        # Check if workflow exists
        if workflow_id not in self.workflows:
            logger.error(f"Workflow {workflow_id} not found")
            return {"status": "error", "message": f"Workflow {workflow_id} not found"}
        
        # Get workflow information
        workflow = self.workflows[workflow_id]
        
        # Store the current phase as completed
        workflow["completed_phases"].append(workflow["current_phase"])
        
        # Update the current phase
        workflow["current_phase"] = next_phase
        
        # Create advance workflow task for orchestrator
        task = self.orchestrator.create_task(
            description=f"Advance workflow to phase: {next_phase}",
            task_type="advance_workflow",
            input_data={"next_phase": next_phase}
        )
        
        # Track the task
        workflow["tasks"][task.task_id] = task.dict()
        
        # Execute the task
        result = self.orchestrator.execute_task(task.task_id)
        
        # Update the task in the workflow
        workflow["tasks"][task.task_id] = task.dict()
        
        # If the task created new tasks, track them as well
        if "new_tasks" in result:
            for new_task in result["new_tasks"]:
                task_id = new_task.get("task_id")
                if task_id:
                    workflow["tasks"][task_id] = new_task
        
        return {
            "status": "advanced",
            "workflow_id": workflow_id,
            "previous_phase": workflow["completed_phases"][-1],
            "current_phase": next_phase,
            "task_id": task.task_id,
            "result": result
        }
    
    async def send_direct_task(self, workflow_id: str, agent_id: str, task_description: str, 
                           task_type: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send a task directly to a specific agent.
        
        Args:
            workflow_id: ID of the workflow
            agent_id: ID of the target agent
            task_description: Description of the task
            task_type: Type of the task
            input_data: Input data for the task
            
        Returns:
            Task delegation result
        """
        logger.info(f"Sending task to agent {agent_id} in workflow {workflow_id}: {task_description}")
        
        # Check if workflow exists
        if workflow_id not in self.workflows:
            logger.error(f"Workflow {workflow_id} not found")
            return {"status": "error", "message": f"Workflow {workflow_id} not found"}
        
        # Get workflow information
        workflow = self.workflows[workflow_id]
        
        # Create a delegation task for the orchestrator
        task = self.orchestrator.create_task(
            description=f"Delegate task to {agent_id}: {task_description}",
            task_type="delegate_task",
            input_data={
                "agent_id": agent_id,
                "description": task_description,
                "task_type": task_type,
                "input_data": input_data
            }
        )
        
        # Track the task
        workflow["tasks"][task.task_id] = task.dict()
        
        # Execute the delegation task
        result = self.orchestrator.execute_task(task.task_id)
        
        # Update the task in the workflow
        workflow["tasks"][task.task_id] = task.dict()
        
        # If a new task was created, track it as well
        if "task" in result:
            task_id = result["task"].get("task_id")
            if task_id:
                workflow["tasks"][task_id] = result["task"]
        
        return {
            "status": "delegated",
            "workflow_id": workflow_id,
            "agent_id": agent_id,
            "task_description": task_description,
            "orchestrator_task_id": task.task_id,
            "result": result
        }
    
    async def collect_task_results(self, workflow_id: str, task_ids: List[str]) -> Dict[str, Any]:
        """Collect results from completed tasks.
        
        Args:
            workflow_id: ID of the workflow
            task_ids: List of task IDs to collect results from
            
        Returns:
            Task results collection
        """
        logger.info(f"Collecting results from {len(task_ids)} tasks in workflow {workflow_id}")
        
        # Check if workflow exists
        if workflow_id not in self.workflows:
            logger.error(f"Workflow {workflow_id} not found")
            return {"status": "error", "message": f"Workflow {workflow_id} not found"}
        
        # Get workflow information
        workflow = self.workflows[workflow_id]
        
        # Create a task to collect results
        task = self.orchestrator.create_task(
            description=f"Collect results from {len(task_ids)} tasks",
            task_type="collect_results",
            input_data={"task_ids": task_ids}
        )
        
        # Track the task
        workflow["tasks"][task.task_id] = task.dict()
        
        # Execute the collection task
        result = self.orchestrator.execute_task(task.task_id)
        
        # Update the task in the workflow
        workflow["tasks"][task.task_id] = task.dict()
        
        # Store any collected documents in the workflow
        if "documents" in result:
            for doc in result["documents"]:
                doc_type = doc.get("document_type")
                if doc_type:
                    workflow["documents"][doc_type] = doc
        
        return {
            "status": "collected",
            "workflow_id": workflow_id,
            "task_id": task.task_id,
            "result": result
        }
    
    def get_workflow_status(self, workflow_id: Optional[str] = None) -> Dict[str, Any]:
        """Get the current status of the workflow.
        
        Args:
            workflow_id: Optional ID of the workflow to get status for.
                         If None, returns status of all workflows.
            
        Returns:
            Workflow status information
        """
        if workflow_id:
            # Check if workflow exists
            if workflow_id not in self.workflows:
                logger.error(f"Workflow {workflow_id} not found")
                return {"status": "error", "message": f"Workflow {workflow_id} not found"}
            
            # Get workflow information
            workflow = self.workflows[workflow_id]
            
            # Get orchestrator status
            orchestrator_status = self.orchestrator.get_workflow_status()
            
            # Combine workflow information with orchestrator status
            status = {
                "workflow_id": workflow_id,
                "name": workflow["name"],
                "status": workflow["status"],
                "current_phase": workflow["current_phase"],
                "completed_phases": workflow["completed_phases"],
                "start_time": workflow["start_time"],
                "tasks": {
                    "total": len(workflow["tasks"]),
                    "completed": sum(1 for t in workflow["tasks"].values() if t.get("status") == "completed"),
                    "in_progress": sum(1 for t in workflow["tasks"].values() if t.get("status") == "in_progress"),
                    "pending": sum(1 for t in workflow["tasks"].values() if t.get("status") == "pending"),
                    "failed": sum(1 for t in workflow["tasks"].values() if t.get("status") == "failed")
                },
                "documents": {
                    "total": len(workflow["documents"]),
                    "types": list(workflow["documents"].keys())
                },
                "agents": orchestrator_status.get("agents", {})
            }
            
            return status
        else:
            # Return status of all workflows
            return {
                "workflows": [
                    {
                        "workflow_id": wf_id,
                        "name": wf["name"],
                        "status": wf["status"],
                        "current_phase": wf["current_phase"],
                        "start_time": wf["start_time"],
                        "task_count": len(wf["tasks"]),
                        "document_count": len(wf["documents"])
                    }
                    for wf_id, wf in self.workflows.items()
                ],
                "agents": self.agent_registry.get_active_agents(),
                "rag_service": self.rag_service.get_stats(),
                "llm_service": self.llm_service.get_usage_stats()
            }
    
    async def finalize_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Finalize the workflow and prepare deliverables.
        
        Args:
            workflow_id: ID of the workflow to finalize
            
        Returns:
            Workflow finalization result
        """
        logger.info(f"Finalizing workflow {workflow_id}")
        
        # Check if workflow exists
        if workflow_id not in self.workflows:
            logger.error(f"Workflow {workflow_id} not found")
            return {"status": "error", "message": f"Workflow {workflow_id} not found"}
        
        # Get workflow information
        workflow = self.workflows[workflow_id]
        
        # Create finalization task for orchestrator
        task = self.orchestrator.create_task(
            description="Finalize project and prepare deliverables",
            task_type="finalize_project",
            input_data={}
        )
        
        # Track the task
        workflow["tasks"][task.task_id] = task.dict()
        
        # Execute the task
        result = self.orchestrator.execute_task(task.task_id)
        
        # Update the task in the workflow
        workflow["tasks"][task.task_id] = task.dict()
        
        # Update workflow status
        workflow["status"] = "completed"
        workflow["completion_time"] = datetime.utcnow().isoformat()
        
        return {
            "status": "finalized",
            "workflow_id": workflow_id,
            "task_id": task.task_id,
            "completion_time": workflow["completion_time"],
            "execution_duration": self._calculate_duration(workflow["start_time"], workflow["completion_time"]),
            "result": result
        }
    
    def _calculate_duration(self, start_time: str, end_time: str) -> str:
        """Calculate the duration between two ISO timestamps."""
        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)
        duration = end - start
        
        # Format duration as hours, minutes, seconds
        hours, remainder = divmod(duration.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
    
    def shutdown(self):
        """Shutdown the workflow service."""
        logger.info("Shutting down Workflow Service")
        
        # Shutdown all active agents
        self.agent_registry.shutdown_all()
        
        # Mark all workflows as stopped
        for workflow_id, workflow in self.workflows.items():
            if workflow["status"] == "active":
                workflow["status"] = "stopped"
                workflow["stop_time"] = datetime.utcnow().isoformat()