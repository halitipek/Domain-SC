import os
import uuid
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable

from src.agents.base_agent import BaseAgent
from src.models.base_models import AgentMessage, AgentTask
from src.utils.logger import setup_logger

logger = setup_logger(__name__, "orchestrator_agent.log")

class OrchestratorAgent(BaseAgent):
    """Orchestrator Agent (OA) for coordinating the multi-agent system."""
    
    def __init__(self, agent_id: str = "OA", name: str = "Orchestrator Agent", 
                 max_tokens: int = 4000):
        super().__init__(agent_id, name, max_tokens)
        
        # Track registered agents
        self.registered_agents = {}
        
        # Track project workflow state
        self.workflow_state = {
            "current_phase": "initialized",
            "completed_phases": [],
            "active_tasks": {},
            "documents": {}
        }
        
        logger.info("Orchestrator Agent initialized")
    
    def register_agent(self, agent_id: str, agent_type: str, capabilities: List[str]) -> None:
        """Register an agent with the orchestrator."""
        self.registered_agents[agent_id] = {
            "agent_type": agent_type,
            "capabilities": capabilities,
            "status": "idle",
            "current_task": None,
            "last_active": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Agent {agent_id} registered with orchestrator")
    
    def unregister_agent(self, agent_id: str) -> None:
        """Unregister an agent."""
        if agent_id in self.registered_agents:
            del self.registered_agents[agent_id]
            logger.info(f"Agent {agent_id} unregistered from orchestrator")
    
    def execute_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Execute an orchestration task."""
        if task_id not in self.tasks:
            logger.error(f"Task {task_id} not found for agent {self.agent_id}")
            return None
            
        task = self.tasks[task_id]
        task.status = "in_progress"
        
        logger.info(f"OA executing task: {task.description}")
        
        result = None
        
        # Handle different orchestration task types
        if task.task_type == "start_workflow":
            # Start the system architecture workflow
            workflow_name = task.input_data.get("workflow_name")
            input_files = task.input_data.get("input_files", [])
            
            result = self._start_workflow(workflow_name, input_files)
            
        elif task.task_type == "advance_workflow":
            # Move workflow to next phase
            next_phase = task.input_data.get("next_phase")
            
            result = self._advance_workflow(next_phase)
            
        elif task.task_type == "delegate_task":
            # Delegate a task to another agent
            agent_id = task.input_data.get("agent_id")
            subtask_desc = task.input_data.get("description")
            subtask_type = task.input_data.get("task_type")
            subtask_data = task.input_data.get("input_data", {})
            
            result = self._delegate_task(agent_id, subtask_desc, subtask_type, subtask_data)
            
        elif task.task_type == "collect_results":
            # Collect results from completed tasks
            task_ids = task.input_data.get("task_ids", [])
            
            result = self._collect_results(task_ids)
            
        elif task.task_type == "finalize_project":
            # Finalize the project and create deliverables
            result = self._finalize_project()
        
        # Update task with result
        if result:
            task.status = "completed"
            task.result = result
        else:
            task.status = "failed"
            task.result = {"error": f"Unknown task type or failed execution: {task.task_type}"}
        
        logger.info(f"OA completed task {task_id} with status {task.status}")
        return task.result
    
    def _start_workflow(self, workflow_name: str, input_files: List[str]) -> Dict[str, Any]:
        """Start a new workflow."""
        logger.info(f"Starting workflow: {workflow_name}")
        
        # Update workflow state
        self.workflow_state["current_phase"] = "document_discovery"
        self.workflow_state["workflow_name"] = workflow_name
        self.workflow_state["start_time"] = datetime.utcnow().isoformat()
        self.workflow_state["input_files"] = input_files
        
        # Create initial tasks for document discovery
        dda_task = self._delegate_task(
            "DDA", 
            "Discover and process input documents", 
            "process_documents", 
            {"file_paths": input_files}
        )
        
        return {
            "status": "success",
            "workflow": workflow_name,
            "current_phase": self.workflow_state["current_phase"],
            "initial_tasks": [dda_task]
        }
    
    def _advance_workflow(self, next_phase: str) -> Dict[str, Any]:
        """Advance the workflow to the next phase."""
        current_phase = self.workflow_state["current_phase"]
        logger.info(f"Advancing workflow from {current_phase} to {next_phase}")
        
        # Store the completed phase
        self.workflow_state["completed_phases"].append(current_phase)
        
        # Update current phase
        self.workflow_state["current_phase"] = next_phase
        
        # Create tasks based on the new phase
        new_tasks = []
        
        if next_phase == "rule_analysis":
            # Create task for KAA
            kaa_task = self._delegate_task(
                "KAA", 
                "Analyze rules from project documents", 
                "analyze_rules", 
                {"documents": self.workflow_state.get("documents", {})}
            )
            new_tasks.append(kaa_task)
            
        elif next_phase == "requirements_analysis":
            # Create task for RAA
            raa_task = self._delegate_task(
                "RAA", 
                "Analyze requirements from project documents", 
                "analyze_requirements", 
                {"documents": self.workflow_state.get("documents", {})}
            )
            new_tasks.append(raa_task)
            
        elif next_phase == "technology_analysis":
            # Create task for TAA
            taa_task = self._delegate_task(
                "TAA", 
                "Analyze technology options for the project", 
                "analyze_technology", 
                {"documents": self.workflow_state.get("documents", {})}
            )
            new_tasks.append(taa_task)
            
        elif next_phase == "optimization_analysis":
            # Create task for OAA
            oaa_task = self._delegate_task(
                "OAA", 
                "Analyze optimization strategies for the project", 
                "analyze_optimization", 
                {"documents": self.workflow_state.get("documents", {})}
            )
            new_tasks.append(oaa_task)
            
        elif next_phase == "architecture_design":
            # Create tasks for SAA and related agents
            saa_task = self._delegate_task(
                "SAA", 
                "Create initial architecture design documents", 
                "create_architecture_document", 
                {
                    "document_type": "SMAP",
                    "input_documents": self.workflow_state.get("documents", {})
                }
            )
            new_tasks.append(saa_task)
            
        elif next_phase == "api_module_design":
            # Create tasks for API and module design
            aea_task = self._delegate_task(
                "AEA", 
                "Design API contracts", 
                "design_api_contracts", 
                {"architecture_docs": self.workflow_state.get("documents", {})}
            )
            
            mta_task = self._delegate_task(
                "MTA", 
                "Design module specifications", 
                "design_modules", 
                {"architecture_docs": self.workflow_state.get("documents", {})}
            )
            
            new_tasks.extend([aea_task, mta_task])
            
        elif next_phase == "finalization":
            # Create final ADD task for SAA
            saa_final_task = self._delegate_task(
                "SAA", 
                "Create complete Architecture Design Document", 
                "create_complete_add", 
                {"input_documents": self.workflow_state.get("documents", {})}
            )
            new_tasks.append(saa_final_task)
        
        return {
            "status": "success",
            "previous_phase": current_phase,
            "current_phase": next_phase,
            "new_tasks": new_tasks
        }
    
    def _delegate_task(self, agent_id: str, description: str, 
                      task_type: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate a task to another agent."""
        # Check if agent is registered
        if agent_id not in self.registered_agents:
            logger.warning(f"Agent {agent_id} is not registered. Cannot delegate task.")
            return {"status": "error", "message": f"Agent {agent_id} not registered"}
        
        # Create a task ID
        task_id = f"{agent_id}_{uuid.uuid4().hex[:8]}"
        
        # Create task object
        task = AgentTask(
            task_id=task_id,
            agent_id=agent_id,
            description=description,
            task_type=task_type,
            input_data=input_data,
            status="pending",
            created_at=datetime.utcnow().isoformat()
        )
        
        # Track task in workflow state
        self.workflow_state["active_tasks"][task_id] = {
            "agent_id": agent_id,
            "description": description,
            "task_type": task_type,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Update agent status
        self.registered_agents[agent_id]["status"] = "assigned"
        self.registered_agents[agent_id]["current_task"] = task_id
        self.registered_agents[agent_id]["last_active"] = datetime.utcnow().isoformat()
        
        # Send task message to agent
        message = self.send_message(
            recipient=agent_id,
            content=task.dict(),  # Convert task to dict for message
            message_type="task"
        )
        
        logger.info(f"Delegated task {task_id} to agent {agent_id}: {description}")
        
        return {
            "status": "delegated",
            "task_id": task_id,
            "agent_id": agent_id,
            "description": description
        }
    
    def _collect_results(self, task_ids: List[str]) -> Dict[str, Any]:
        """Collect results from completed tasks."""
        logger.info(f"Collecting results from {len(task_ids)} tasks")
        
        results = {}
        missing_tasks = []
        
        for task_id in task_ids:
            # Check if task is in workflow state
            if task_id in self.workflow_state["active_tasks"]:
                task_info = self.workflow_state["active_tasks"][task_id]
                agent_id = task_info["agent_id"]
                
                # Request result from agent
                # In a real system, this would use a message passing mechanism
                # For simplicity, we'll assume we can get the task directly
                
                if agent_id in self.registered_agents:
                    # In a real implementation, we'd query the agent for the task result
                    # Here we'll just use what we have in our workflow state
                    
                    if task_info["status"] == "completed":
                        results[task_id] = task_info.get("result", {})
                        
                        # If this task produced a document, store it
                        if "document" in results[task_id]:
                            doc_type = results[task_id].get("document_type", "unknown")
                            doc_content = results[task_id]["document"]
                            self.workflow_state["documents"][doc_type] = doc_content
                    else:
                        missing_tasks.append(task_id)
                else:
                    missing_tasks.append(task_id)
            else:
                missing_tasks.append(task_id)
        
        return {
            "status": "success",
            "collected_results": len(results),
            "missing_tasks": missing_tasks,
            "results": results
        }
    
    def _finalize_project(self) -> Dict[str, Any]:
        """Finalize the project and prepare deliverables."""
        logger.info("Finalizing project")
        
        # Collect all documents
        documents = self.workflow_state.get("documents", {})
        
        # Create a zip archive (in a real implementation)
        # Here we'll just return the document list
        
        return {
            "status": "success",
            "document_count": len(documents),
            "document_types": list(documents.keys()),
            "completion_time": datetime.utcnow().isoformat()
        }
    
    def receive_message(self, message: AgentMessage) -> None:
        """Process a received message with special handling for task results."""
        super().receive_message(message)
        
        # Additional processing for task results
        if message.message_type == "task_result":
            task_id = message.content.get("task_id") if isinstance(message.content, dict) else None
            
            if task_id and task_id in self.workflow_state["active_tasks"]:
                # Update task status
                task_info = self.workflow_state["active_tasks"][task_id]
                task_info["status"] = "completed"
                task_info["completed_at"] = datetime.utcnow().isoformat()
                task_info["result"] = message.content.get("result", {})
                
                # Update agent status
                agent_id = task_info["agent_id"]
                if agent_id in self.registered_agents:
                    self.registered_agents[agent_id]["status"] = "idle"
                    self.registered_agents[agent_id]["current_task"] = None
                    self.registered_agents[agent_id]["last_active"] = datetime.utcnow().isoformat()
                
                logger.info(f"Updated task {task_id} status to completed")
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get the current status of the workflow."""
        active_count = sum(1 for task in self.workflow_state["active_tasks"].values() 
                        if task["status"] == "pending" or task["status"] == "in_progress")
        
        completed_count = sum(1 for task in self.workflow_state["active_tasks"].values() 
                           if task["status"] == "completed")
        
        return {
            "workflow_name": self.workflow_state.get("workflow_name", "unknown"),
            "current_phase": self.workflow_state["current_phase"],
            "completed_phases": self.workflow_state["completed_phases"],
            "active_agents": sum(1 for agent in self.registered_agents.values() 
                               if agent["status"] != "idle"),
            "total_agents": len(self.registered_agents),
            "active_tasks": active_count,
            "completed_tasks": completed_count,
            "document_count": len(self.workflow_state.get("documents", {})),
            "document_types": list(self.workflow_state.get("documents", {}).keys())
        }
