"""
Unit tests for the base agent.
"""

import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from pathlib import Path

# Add project root to Python path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.agents.base_agent import BaseAgent
from src.models.base_models import AgentMessage, AgentTask, AgentQuery, AgentResponse


class TestBaseAgent(unittest.TestCase):
    """Tests for the BaseAgent class."""
    
    def setUp(self):
        """Set up test environment."""
        self.agent = BaseAgent(agent_id="TEST", name="Test Agent", max_tokens=1000)
        
        # Set up callback mocks
        self.message_sent_callback = MagicMock()
        self.message_received_callback = MagicMock()
        self.task_created_callback = MagicMock()
        self.task_started_callback = MagicMock()
        self.task_completed_callback = MagicMock()
        self.agent_shutdown_callback = MagicMock()
        
        # Register callbacks
        self.agent.register_callback("message_sent", self.message_sent_callback)
        self.agent.register_callback("message_received", self.message_received_callback)
        self.agent.register_callback("task_created", self.task_created_callback)
        self.agent.register_callback("task_started", self.task_started_callback)
        self.agent.register_callback("task_completed", self.task_completed_callback)
        self.agent.register_callback("agent_shutdown", self.agent_shutdown_callback)
    
    def test_initialization(self):
        """Test initialization of the BaseAgent."""
        self.assertEqual(self.agent.agent_id, "TEST")
        self.assertEqual(self.agent.name, "Test Agent")
        self.assertEqual(self.agent.max_tokens, 1000)
        self.assertEqual(self.agent.memory, [])
        self.assertEqual(self.agent.tasks, {})
        self.assertTrue(self.agent.active)
    
    def test_register_callback(self):
        """Test registering a callback."""
        # Test existing callbacks
        self.assertEqual(self.agent.callbacks["message_sent"], self.message_sent_callback)
        self.assertEqual(self.agent.callbacks["message_received"], self.message_received_callback)
        self.assertEqual(self.agent.callbacks["task_created"], self.task_created_callback)
        self.assertEqual(self.agent.callbacks["task_started"], self.task_started_callback)
        self.assertEqual(self.agent.callbacks["task_completed"], self.task_completed_callback)
        self.assertEqual(self.agent.callbacks["agent_shutdown"], self.agent_shutdown_callback)
        
        # Test registering a new callback
        new_callback = MagicMock()
        self.agent.register_callback("new_event", new_callback)
        self.assertEqual(self.agent.callbacks["new_event"], new_callback)
    
    def test_send_message(self):
        """Test sending a message."""
        # Send a message
        message = self.agent.send_message(
            recipient="RECIPIENT",
            content="Test message",
            message_type="text",
            references=["ref1", "ref2"]
        )
        
        # Verify message
        self.assertEqual(message.sender, "TEST")
        self.assertEqual(message.recipient, "RECIPIENT")
        self.assertEqual(message.content, "Test message")
        self.assertEqual(message.message_type, "text")
        self.assertEqual(message.references, ["ref1", "ref2"])
        self.assertIsNotNone(message.timestamp)
        
        # Verify callback was called
        self.message_sent_callback.assert_called_once()
        self.assertEqual(self.message_sent_callback.call_args[0][0], message)
    
    def test_receive_message(self):
        """Test receiving a message."""
        # Create a message
        message = AgentMessage(
            sender="SENDER",
            recipient="TEST",
            content="Test message",
            message_type="text",
            timestamp=datetime.utcnow().isoformat(),
            references=[]
        )
        
        # Receive the message
        self.agent.receive_message(message)
        
        # Verify message was stored
        self.assertEqual(len(self.agent.memory), 1)
        self.assertEqual(self.agent.memory[0], message)
        
        # Verify callback was called
        self.message_received_callback.assert_called_once()
        self.assertEqual(self.message_received_callback.call_args[0][0], message)
    
    def test_receive_task_message(self):
        """Test receiving a task message."""
        # Create a task
        task = AgentTask(
            task_id="test_task",
            agent_id="TEST",
            description="Test task",
            task_type="test_type",
            input_data={"key": "value"},
            status="pending"
        )
        
        # Create a task message
        message = AgentMessage(
            sender="SENDER",
            recipient="TEST",
            content=task.dict(),
            message_type="task",
            timestamp=datetime.utcnow().isoformat(),
            references=[]
        )
        
        # Mock the receive_task method
        self.agent.receive_task = MagicMock()
        
        # Receive the message
        self.agent.receive_message(message)
        
        # Verify receive_task was called
        self.agent.receive_task.assert_called_once()
        self.assertEqual(self.agent.receive_task.call_args[0][0].task_id, task.task_id)
    
    def test_receive_query_message(self):
        """Test receiving a query message."""
        # Create a query
        query = AgentQuery(
            query_id="test_query",
            sender="SENDER",
            recipient="TEST",
            content="Test query",
            context={"key": "value"},
            timestamp=datetime.utcnow().isoformat()
        )
        
        # Create a query message
        message = AgentMessage(
            sender="SENDER",
            recipient="TEST",
            content=query.dict(),
            message_type="query",
            timestamp=datetime.utcnow().isoformat(),
            references=[]
        )
        
        # Mock the process_query method
        self.agent.process_query = MagicMock()
        
        # Receive the message
        self.agent.receive_message(message)
        
        # Verify process_query was called
        self.agent.process_query.assert_called_once()
        self.assertEqual(self.agent.process_query.call_args[0][0].query_id, query.query_id)
    
    def test_create_task(self):
        """Test creating a task."""
        # Create a task
        task = self.agent.create_task(
            description="Test task",
            task_type="test_type",
            input_data={"key": "value"},
            priority=2,
            dependencies=["dep1", "dep2"]
        )
        
        # Verify task
        self.assertEqual(task.agent_id, "TEST")
        self.assertEqual(task.description, "Test task")
        self.assertEqual(task.task_type, "test_type")
        self.assertEqual(task.input_data, {"key": "value"})
        self.assertEqual(task.status, "pending")
        self.assertEqual(task.priority, 2)
        self.assertEqual(task.dependencies, ["dep1", "dep2"])
        self.assertIsNotNone(task.created_at)
        self.assertIsNotNone(task.updated_at)
        
        # Verify task was stored
        self.assertIn(task.task_id, self.agent.tasks)
        self.assertEqual(self.agent.tasks[task.task_id], task)
        
        # Verify callback was called
        self.task_created_callback.assert_called_once()
        self.assertEqual(self.task_created_callback.call_args[0][0], task)
    
    def test_receive_task(self):
        """Test receiving a task."""
        # Create a task
        task = AgentTask(
            task_id="test_task",
            agent_id="TEST",
            description="Test task",
            task_type="test_type",
            input_data={"key": "value"},
            status="pending",
            dependencies=[]
        )
        
        # Mock the execute_task method
        self.agent.execute_task = MagicMock()
        
        # Receive the task
        self.agent.receive_task(task)
        
        # Verify task was stored
        self.assertIn(task.task_id, self.agent.tasks)
        self.assertEqual(self.agent.tasks[task.task_id], task)
        
        # Verify execute_task was called
        self.agent.execute_task.assert_called_once_with(task.task_id)
    
    def test_receive_task_with_dependencies(self):
        """Test receiving a task with dependencies."""
        # Create a dependency task (not completed)
        dep_task = AgentTask(
            task_id="dep_task",
            agent_id="TEST",
            description="Dependency task",
            task_type="test_type",
            input_data={},
            status="pending"
        )
        
        # Store the dependency task
        self.agent.tasks[dep_task.task_id] = dep_task
        
        # Create a task with the dependency
        task = AgentTask(
            task_id="test_task",
            agent_id="TEST",
            description="Test task",
            task_type="test_type",
            input_data={},
            status="pending",
            dependencies=["dep_task"]
        )
        
        # Mock the execute_task method
        self.agent.execute_task = MagicMock()
        
        # Receive the task
        self.agent.receive_task(task)
        
        # Verify task was stored
        self.assertIn(task.task_id, self.agent.tasks)
        self.assertEqual(self.agent.tasks[task.task_id], task)
        
        # Verify execute_task was not called (dependency not completed)
        self.agent.execute_task.assert_not_called()
        
        # Complete the dependency task
        dep_task.status = "completed"
        
        # Receive the task again
        self.agent.receive_task(task)
        
        # Verify execute_task was called
        self.agent.execute_task.assert_called_once_with(task.task_id)
    
    def test_execute_task(self):
        """Test executing a task."""
        # Create a task
        task = AgentTask(
            task_id="test_task",
            agent_id="TEST",
            description="Test task",
            task_type="test_type",
            input_data={},
            status="pending"
        )
        
        # Store the task
        self.agent.tasks[task.task_id] = task
        
        # Execute the task
        result = self.agent.execute_task(task.task_id)
        
        # Verify task status was updated
        self.assertEqual(task.status, "completed")
        self.assertIsNotNone(task.result)
        self.assertIsNotNone(task.updated_at)
        
        # Verify callbacks were called
        self.task_started_callback.assert_called_once()
        self.assertEqual(self.task_started_callback.call_args[0][0], task)
        
        self.task_completed_callback.assert_called_once()
        self.assertEqual(self.task_completed_callback.call_args[0][0], task)
        
        # Verify result
        self.assertEqual(result, {"status": "executed", "message": "Base implementation does nothing"})
    
    def test_execute_nonexistent_task(self):
        """Test executing a nonexistent task."""
        # Execute a nonexistent task
        result = self.agent.execute_task("nonexistent_task")
        
        # Verify result
        self.assertIsNone(result)
    
    def test_query(self):
        """Test querying another agent."""
        # Query another agent
        response = self.agent.query(
            recipient="RECIPIENT",
            content="Test query",
            context={"key": "value"}
        )
        
        # Verify response (this is just a placeholder in the base implementation)
        self.assertIn("Response to query: Test query", response)
    
    def test_process_query(self):
        """Test processing a query."""
        # Create a query
        query = AgentQuery(
            query_id="test_query",
            sender="SENDER",
            recipient="TEST",
            content="Test query",
            context={}
        )
        
        # Process the query
        response = self.agent.process_query(query)
        
        # Verify response
        self.assertEqual(response.query_id, query.query_id)
        self.assertEqual(response.sender, "TEST")
        self.assertEqual(response.recipient, "SENDER")
        self.assertEqual(response.content, "Received your query: Test query")
    
    def test_shutdown(self):
        """Test shutting down the agent."""
        # Shutdown the agent
        self.agent.shutdown()
        
        # Verify agent is inactive
        self.assertFalse(self.agent.active)
        
        # Verify callback was called
        self.agent_shutdown_callback.assert_called_once_with("TEST")
    
    def test_get_memory_summary(self):
        """Test getting a memory summary."""
        # Create some messages and tasks
        message = AgentMessage(
            sender="SENDER",
            recipient="TEST",
            content="Test message",
            message_type="text"
        )
        self.agent.memory.append(message)
        
        pending_task = AgentTask(
            task_id="pending_task",
            agent_id="TEST",
            description="Pending task",
            task_type="test_type",
            status="pending"
        )
        self.agent.tasks[pending_task.task_id] = pending_task
        
        in_progress_task = AgentTask(
            task_id="in_progress_task",
            agent_id="TEST",
            description="In progress task",
            task_type="test_type",
            status="in_progress"
        )
        self.agent.tasks[in_progress_task.task_id] = in_progress_task
        
        completed_task = AgentTask(
            task_id="completed_task",
            agent_id="TEST",
            description="Completed task",
            task_type="test_type",
            status="completed"
        )
        self.agent.tasks[completed_task.task_id] = completed_task
        
        failed_task = AgentTask(
            task_id="failed_task",
            agent_id="TEST",
            description="Failed task",
            task_type="test_type",
            status="failed"
        )
        self.agent.tasks[failed_task.task_id] = failed_task
        
        # Get memory summary
        summary = self.agent.get_memory_summary()
        
        # Verify summary
        self.assertEqual(summary["message_count"], 1)
        self.assertEqual(summary["task_count"], 4)
        self.assertEqual(summary["active_tasks"], 2)  # pending + in_progress
        self.assertEqual(summary["completed_tasks"], 1)
        self.assertEqual(summary["failed_tasks"], 1)


if __name__ == "__main__":
    unittest.main()