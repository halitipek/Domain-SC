"""
Agent Registry for the Domain-SC system.
This module manages agent registration, creation, and tracking.
"""

import logging
from typing import Dict, Any, Optional, Type, List

from src.utils.logger import setup_logger
from src.agents.base_agent import BaseAgent
from src.agents.orchestrator_agent import OrchestratorAgent
from src.agents.system_architect_agent import SystemArchitectAgent
from src.agents.requirements_agent import RequirementsAnalysisAgent
from src.agents.technology_agent import TechnologyAnalysisAgent
from src.agents.optimization_agent import OptimizationAnalysisAgent

logger = setup_logger(__name__, "agent_registry.log")

class AgentRegistry:
    """Registry for managing agents in the system."""
    
    def __init__(self):
        """Initialize the agent registry."""
        # Dictionary of agent class implementations
        self.agent_classes: Dict[str, Type[BaseAgent]] = {
            "OA": OrchestratorAgent,
            "SAA": SystemArchitectAgent,
            "RAA": RequirementsAnalysisAgent,
            "TAA": TechnologyAnalysisAgent,
            "OAA": OptimizationAnalysisAgent,
            # Additional agent types can be registered here
        }
        
        # Dictionary of active agent instances
        self.active_agents: Dict[str, BaseAgent] = {}
        
        # Dictionary of agent capabilities
        self.agent_capabilities: Dict[str, List[str]] = {
            "OA": ["orchestration", "task_delegation", "workflow_management"],
            "SAA": ["architecture_design", "dependency_analysis", "system_design"],
            "RAA": ["requirements_analysis", "requirements_extraction", "domain_modeling"],
            "TAA": ["technology_analysis", "technology_evaluation", "tool_selection"],
            "OAA": ["performance_optimization", "scalability_planning", "cost_optimization"],
            # Additional capabilities can be defined here
        }
        
        logger.info(f"Agent Registry initialized with {len(self.agent_classes)} agent types")
    
    def register_agent_class(self, agent_id: str, agent_class: Type[BaseAgent], 
                           capabilities: List[str]) -> None:
        """Register a new agent class.
        
        Args:
            agent_id: The ID of the agent (e.g., "SAA", "RAA")
            agent_class: The agent class implementation
            capabilities: List of agent capabilities
        """
        if agent_id in self.agent_classes:
            logger.warning(f"Agent class {agent_id} already registered, overwriting")
        
        self.agent_classes[agent_id] = agent_class
        self.agent_capabilities[agent_id] = capabilities
        
        logger.info(f"Registered agent class {agent_id} with capabilities: {', '.join(capabilities)}")
    
    def create_agent(self, agent_id: str, **kwargs) -> Optional[BaseAgent]:
        """Create an agent instance.
        
        Args:
            agent_id: The ID of the agent to create
            **kwargs: Additional arguments to pass to the agent constructor
            
        Returns:
            Agent instance or None if the agent class is not registered
        """
        if agent_id not in self.agent_classes:
            logger.error(f"Agent class {agent_id} not registered")
            return None
        
        # Check if agent already exists
        if agent_id in self.active_agents:
            logger.warning(f"Agent {agent_id} already active, returning existing instance")
            return self.active_agents[agent_id]
        
        # Create a new instance of the agent
        agent_class = self.agent_classes[agent_id]
        agent = agent_class(agent_id=agent_id, **kwargs)
        
        # Store in active agents
        self.active_agents[agent_id] = agent
        
        logger.info(f"Created agent instance {agent_id}")
        return agent
    
    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """Get an active agent instance.
        
        Args:
            agent_id: The ID of the agent to get
            
        Returns:
            Agent instance or None if not active
        """
        if agent_id not in self.active_agents:
            logger.warning(f"Agent {agent_id} not active")
            return None
        
        return self.active_agents[agent_id]
    
    def get_agent_by_capability(self, capability: str) -> Optional[BaseAgent]:
        """Get an agent instance by capability.
        
        Args:
            capability: The capability to look for
            
        Returns:
            Agent instance or None if no agent has the capability
        """
        # Find agent IDs that have the capability
        matching_ids = [
            agent_id for agent_id, capabilities in self.agent_capabilities.items()
            if capability in capabilities
        ]
        
        if not matching_ids:
            logger.warning(f"No agent found with capability: {capability}")
            return None
        
        # Return the first active agent with the capability
        for agent_id in matching_ids:
            if agent_id in self.active_agents:
                return self.active_agents[agent_id]
        
        # If no active agent has the capability, create the first matching one
        return self.create_agent(matching_ids[0])
    
    def shutdown_agent(self, agent_id: str) -> bool:
        """Shutdown an active agent.
        
        Args:
            agent_id: The ID of the agent to shutdown
            
        Returns:
            True if successful, False otherwise
        """
        if agent_id not in self.active_agents:
            logger.warning(f"Agent {agent_id} not active, cannot shutdown")
            return False
        
        # Get the agent instance
        agent = self.active_agents[agent_id]
        
        # Shutdown the agent
        agent.shutdown()
        
        # Remove from active agents
        del self.active_agents[agent_id]
        
        logger.info(f"Shutdown agent {agent_id}")
        return True
    
    def get_active_agents(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all active agents.
        
        Returns:
            Dictionary with agent information
        """
        return {
            agent_id: {
                "type": agent.__class__.__name__,
                "capabilities": self.agent_capabilities.get(agent_id, []),
                "status": "active" if agent.active else "inactive",
                "memory_stats": agent.get_memory_summary()
            }
            for agent_id, agent in self.active_agents.items()
        }
    
    def shutdown_all(self) -> None:
        """Shutdown all active agents."""
        for agent_id in list(self.active_agents.keys()):
            self.shutdown_agent(agent_id)
        
        logger.info(f"Shutdown all active agents")
    
    def initialize_core_agents(self) -> Dict[str, BaseAgent]:
        """Initialize core agents needed for the system.
        
        Returns:
            Dictionary of initialized agents
        """
        # Create orchestrator agent
        oa = self.create_agent("OA")
        
        # Other core agents can be initialized here if needed
        
        return {
            "OA": oa
        }