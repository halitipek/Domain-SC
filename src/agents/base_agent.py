import os
import uuid
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable, Union

from src.utils.logger import setup_logger
from src.models.base_models import AgentMessage, AgentTask, AgentQuery, AgentResponse

logger = setup_logger(__name__, "agents.log")

class BaseAgent:
    """Base class for all agents in the system."""
    
    def __init__(self, agent_id: str, name: str, max_tokens: int = 4000):
        self.agent_id = agent_id
        self.name = name
        self.max_tokens = max_tokens
        self.memory = []  # Simple memory to store messages and context
        self.tasks = {}  # Dictionary to store tasks by ID
        self.callbacks = {}  # Dictionary to store callback functions
        self.active = True
        
    def register_callback(self, event: str, callback: Callable) -> None:
        """Register a callback function for a specific event."""
        self.callbacks[event] = callback
        
    def send_message(self, recipient: str, content: Union[str, Dict[str, Any]], 
                     message_type: str = "text", references: List[str] = None) -> AgentMessage:
        """Send a message to another agent."""
        if references is None:
            references = []
            
        message = AgentMessage(
            sender=self.agent_id,
            recipient=recipient,
            content=content,
            message_type=message_type,
            timestamp=datetime.utcnow().isoformat(),
            references=references
        )
        
        if "message_sent" in self.callbacks:
            self.callbacks["message_sent"](message)
            
        logger.info(f"Agent {self.agent_id} sent message to {recipient}")
        return message
    
    def receive_message(self, message: AgentMessage) -> None:
        """Process a received message."""
        if not self.active:
            logger.warning(f"Agent {self.agent_id} is inactive. Message not processed.")
            return
            
        # Store message in memory
        self.memory.append(message)
        
        if "message_received" in self.callbacks:
            self.callbacks["message_received"](message)
        
        logger.info(f"Agent {self.agent_id} received message from {message.sender}")
        
        # Process the message based on type
        if message.message_type == "task":            
            # Convert message content to task if needed
            if isinstance(message.content, dict):
                task = AgentTask(**message.content)
            else:
                task_content = json.loads(message.content) if isinstance(message.content, str) else {}
                task = AgentTask(**task_content)
                
            self.receive_task(task)
        elif message.message_type == "query":
            # Handle query message
            if isinstance(message.content, dict):
                query = AgentQuery(**message.content)
            else:
                query_content = json.loads(message.content) if isinstance(message.content, str) else {}
                query = AgentQuery(**query_content)
                
            self.process_query(query)
    
    def create_task(self, description: str, task_type: str, 
                   input_data: Dict[str, Any] = None, priority: int = 1,
                   dependencies: List[str] = None) -> AgentTask:
        """Create a new task for this agent."""
        if input_data is None:
            input_data = {}
        if dependencies is None:
            dependencies = []
            
        task_id = f"{self.agent_id}_{uuid.uuid4().hex[:8]}"  
        
        task = AgentTask(
            task_id=task_id,
            agent_id=self.agent_id,
            description=description,
            task_type=task_type,
            input_data=input_data,
            status="pending",
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat(),
            priority=priority,
            dependencies=dependencies
        )
        
        self.tasks[task_id] = task
        
        if "task_created" in self.callbacks:
            self.callbacks["task_created"](task)
            
        logger.info(f"Agent {self.agent_id} created task {task_id}: {description}")
        return task
    
    def receive_task(self, task: AgentTask) -> None:
        """Receive and process a task."""
        if not self.active:
            logger.warning(f"Agent {self.agent_id} is inactive. Task not processed.")
            return
            
        # Store task
        self.tasks[task.task_id] = task
        
        # Check if dependencies are fulfilled
        can_execute = True
        for dep_id in task.dependencies:
            if dep_id not in self.tasks or self.tasks[dep_id].status != "completed":
                can_execute = False
                break
                
        if can_execute:
            self.execute_task(task.task_id)
        
        logger.info(f"Agent {self.agent_id} received task {task.task_id}")
    
    def execute_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Execute a task by its ID. Should be implemented by subclasses.
        
        Args:
            task_id: The ID of the task to execute
            
        Returns:
            Task result dictionary if successful, None if task not found
        """
        if not task_id or not isinstance(task_id, str):
            logger.error(f"Invalid task_id: {task_id}")
            return None
            
        if task_id not in self.tasks:
            logger.error(f"Task {task_id} not found for agent {self.agent_id}")
            return None
            
        task = self.tasks[task_id]
        
        # Check if task is already completed
        if task.status == "completed":
            logger.info(f"Task {task_id} already completed, returning existing result")
            return task.result
            
        # Update task status
        task.status = "in_progress"
        task.updated_at = datetime.utcnow().isoformat()
        
        try:
            # Call task_started callback if registered
            if "task_started" in self.callbacks and callable(self.callbacks["task_started"]):
                self.callbacks["task_started"](task)
                
            logger.info(f"Agent {self.agent_id} started executing task {task_id}")
            
            # Check dependencies before execution
            if hasattr(task, 'dependencies') and task.dependencies:
                for dep_id in task.dependencies:
                    if dep_id not in self.tasks:
                        logger.warning(f"Dependency {dep_id} for task {task_id} not found")
                        task.status = "waiting_for_dependencies"
                        return None
                    if self.tasks[dep_id].status != "completed":
                        logger.warning(f"Dependency {dep_id} for task {task_id} not completed")
                        task.status = "waiting_for_dependencies"
                        return None
            
            # This should be overridden by subclasses
            result = {"status": "executed", "message": "Base implementation does nothing"}
            
            # Update task with result
            task.status = "completed"
            task.result = result
            task.updated_at = datetime.utcnow().isoformat()
            
            # Call task_completed callback if registered
            if "task_completed" in self.callbacks and callable(self.callbacks["task_completed"]):
                self.callbacks["task_completed"](task)
                
            logger.info(f"Agent {self.agent_id} completed task {task_id}")
            return result
            
        except Exception as e:
            error_msg = f"Error executing task {task_id}: {str(e)}"
            logger.error(error_msg)
            
            # Update task with error
            task.status = "failed"
            task.result = {"status": "failed", "error": error_msg}
            task.updated_at = datetime.utcnow().isoformat()
            
            # Call task_failed callback if registered
            if "task_failed" in self.callbacks and callable(self.callbacks["task_failed"]):
                self.callbacks["task_failed"](task)
                
            return task.result
    
    def query(self, recipient: str, content: str, context: Dict[str, Any] = None) -> str:
        """Send a query to another agent and get response."""
        if context is None:
            context = {}
            
        query_id = f"{self.agent_id}_{uuid.uuid4().hex[:8]}"
        
        query = AgentQuery(
            query_id=query_id,
            sender=self.agent_id,
            recipient=recipient,
            content=content,
            context=context,
            timestamp=datetime.utcnow().isoformat()
        )
        
        # This would typically use an async approach or callback mechanism in a real system
        # For simplicity, we're using a synchronous placeholder
        logger.info(f"Agent {self.agent_id} sent query to {recipient}: {content[:50]}...")
        
        # In a real implementation, this would send the query and wait for response
        response = f"Response to query: {content[:20]}..."
        
        return response
    
    def process_query(self, query: AgentQuery) -> AgentResponse:
        """Process a query from another agent. Should be implemented by subclasses.
        
        Args:
            query: The query to process
            
        Returns:
            Response to the query
        """
        if not isinstance(query, AgentQuery):
            logger.error(f"Invalid query object type: {type(query)}")
            return AgentResponse(
                query_id=getattr(query, 'query_id', 'unknown'),
                sender=self.agent_id,
                recipient=getattr(query, 'sender', 'unknown'),
                content="Error: Invalid query format",
                timestamp=datetime.utcnow().isoformat()
            )
            
        if not query.content:
            logger.warning(f"Empty query content from {query.sender}")
            
        try:
            # Default implementation just echoes the query
            safe_content = query.content
            if isinstance(safe_content, str) and len(safe_content) > 100:
                safe_content = f"{safe_content[:100]}..."
                
            response = AgentResponse(
                query_id=query.query_id,
                sender=self.agent_id,
                recipient=query.sender,
                content=f"Received your query: {safe_content}",
                timestamp=datetime.utcnow().isoformat()
            )
            
            logger.info(f"Agent {self.agent_id} processed query from {query.sender}")
            return response
            
        except Exception as e:
            error_msg = f"Error processing query: {str(e)}"
            logger.error(error_msg)
            
            return AgentResponse(
                query_id=query.query_id,
                sender=self.agent_id,
                recipient=query.sender,
                content=f"Error: {error_msg}",
                timestamp=datetime.utcnow().isoformat()
            )
    
    def shutdown(self) -> None:
        """Gracefully shutdown the agent."""
        self.active = False
        logger.info(f"Agent {self.agent_id} is shutting down")
        
        if "agent_shutdown" in self.callbacks:
            self.callbacks["agent_shutdown"](self.agent_id)
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Get a summary of the agent's memory."""
        return {
            "message_count": len(self.memory),
            "task_count": len(self.tasks),
            "active_tasks": sum(1 for t in self.tasks.values() if t.status in ["pending", "in_progress"]),
            "completed_tasks": sum(1 for t in self.tasks.values() if t.status == "completed"),
            "failed_tasks": sum(1 for t in self.tasks.values() if t.status == "failed")
        }
