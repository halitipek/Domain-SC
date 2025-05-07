"""
Integration tests for agent interactions.

These tests ensure that different agents can communicate
and collaborate correctly.
"""

import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path

# Add project root to Python path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.agents.base_agent import BaseAgent
from src.agents.orchestrator_agent import OrchestratorAgent
from src.agents.system_architect_agent import SystemArchitectAgent
from src.models.base_models import AgentMessage, AgentTask, AgentQuery, AgentResponse


class TestAgentInteraction(unittest.TestCase):
    """Integration tests for agent interactions."""
    
    def setUp(self):
        """Set up test environment."""
        # Create the agents
        self.orchestrator = OrchestratorAgent()
        self.saa = SystemArchitectAgent()
        
        # Set up the interaction
        self.orchestrator.register_agent(
            agent_id="SAA",
            agent_type="system_architect",
            capabilities=["architecture_design", "system_design"]
        )
        
        # Mock RAG service in SAA to avoid actual vector DB operations
        self.mock_rag_service = MagicMock()
        self.mock_rag_query_result = MagicMock()
        self.mock_rag_query_result.answer = "This is a mock RAG response about architecture."
        self.mock_rag_query_result.retrieved_documents = []
        self.mock_rag_service.query.return_value = self.mock_rag_query_result
        self.saa.rag_service = self.mock_rag_service
    
    def test_task_delegation_and_execution(self):
        """Test delegating a task from orchestrator to SAA and execution."""
        # Create a mock for the SAA's execute_task method to capture the task
        original_execute_task = self.saa.execute_task
        executed_task = [None]  # Use a list to store the task (for closure access)
        
        def mock_execute_task(task_id):
            """Mock execute_task to capture the task and call the original method."""
            task = self.saa.tasks.get(task_id)
            executed_task[0] = task
            return original_execute_task(task_id)
        
        self.saa.execute_task = mock_execute_task
        
        # Set up message delivery
        def deliver_message(message):
            """Deliver message from orchestrator to SAA."""
            if message.recipient == "SAA":
                self.saa.receive_message(message)
        
        # Configure orchestrator to use our message delivery function
        self.orchestrator.send_message = MagicMock(side_effect=deliver_message)
        
        # Create a task to delegate
        task = self.orchestrator.create_task(
            description="Delegate task to SAA",
            task_type="delegate_task",
            input_data={
                "agent_id": "SAA",
                "description": "Create an architecture document",
                "task_type": "create_architecture_document",
                "input_data": {
                    "document_type": "SMAP",
                    "input_documents": {"requirements": "Sample requirements"}
                }
            }
        )
        
        # Execute the delegation task
        result = self.orchestrator.execute_task(task.task_id)
        
        # Verify the task was delegated
        self.assertEqual(result["status"], "delegated")
        self.assertEqual(result["agent_id"], "SAA")
        
        # Verify the SAA received and executed the task
        self.assertIsNotNone(executed_task[0])
        self.assertEqual(executed_task[0].task_type, "create_architecture_document")
        self.assertEqual(executed_task[0].input_data["document_type"], "SMAP")
        
        # Verify the RAG service was used
        self.mock_rag_service.query.assert_called()
    
    def test_query_and_response(self):
        """Test querying the SAA from the orchestrator and getting a response."""
        # Set up direct access to both agents for this test
        # (bypassing the message passing for simplicity)
        
        # Create a query
        query = AgentQuery(
            query_id="test_query",
            sender="OA",
            recipient="SAA",
            content="What is the best architecture for a distributed system?",
            context={}
        )
        
        # Process the query with SAA
        response = self.saa.process_query(query)
        
        # Verify response
        self.assertEqual(response.query_id, query.query_id)
        self.assertEqual(response.sender, "SAA")
        self.assertEqual(response.recipient, "OA")
        self.assertIn("Based on architectural best practices", response.content)
        
        # Verify RAG service was used
        self.mock_rag_service.query.assert_called_with(
            query.content, agent_type="SAA"
        )
    
    def test_workflow_phase_transition(self):
        """Test advancing workflow phases and creating appropriate tasks."""
        # Set up message delivery
        delivered_messages = []
        
        def deliver_message(recipient, content, message_type="text", references=None):
            """Mock send_message to capture the message."""
            message = AgentMessage(
                sender="OA",
                recipient=recipient,
                content=content,
                message_type=message_type,
                references=references if references else []
            )
            delivered_messages.append(message)
            return message
        
        # Configure orchestrator to use our message delivery function
        self.orchestrator.send_message = MagicMock(side_effect=deliver_message)
        
        # Initialize workflow state
        self.orchestrator.workflow_state = {
            "current_phase": "requirements_analysis",
            "completed_phases": ["document_discovery"],
            "active_tasks": {},
            "documents": {}
        }
        
        # Create a task to advance the workflow
        task = self.orchestrator.create_task(
            description="Advance workflow to architecture_design phase",
            task_type="advance_workflow",
            input_data={"next_phase": "architecture_design"}
        )
        
        # Execute the task
        result = self.orchestrator.execute_task(task.task_id)
        
        # Verify the workflow phase was advanced
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["current_phase"], "architecture_design")
        self.assertEqual(result["previous_phase"], "requirements_analysis")
        
        # Verify new tasks were created
        self.assertGreater(len(result["new_tasks"]), 0)
        
        # Verify messages were sent (at least one task delegation)
        self.assertGreater(len(delivered_messages), 0)
        found_task_message = False
        for message in delivered_messages:
            if message.message_type == "task" and message.recipient == "SAA":
                found_task_message = True
                break
        self.assertTrue(found_task_message, "No task message sent to SAA")


if __name__ == "__main__":
    unittest.main()