"""
Prompt manager for the Domain-SC system.
This module handles the loading, formatting, and management of prompts for all agents.
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path

from src.utils.logger import setup_logger

logger = setup_logger(__name__, "prompt_manager.log")

class PromptManager:
    """Manages structured prompts for all agents in the system."""
    
    def __init__(self, prompts_dir: Optional[str] = None):
        """Initialize the PromptManager.
        
        Args:
            prompts_dir: Directory containing prompt templates. If None, uses default.
        """
        if prompts_dir:
            self.prompts_dir = Path(prompts_dir)
        else:
            self.prompts_dir = Path(__file__).resolve().parent / "templates"
        
        # Ensure the prompts directory exists
        self.prompts_dir.mkdir(exist_ok=True)
        
        # Dictionary to store loaded prompt templates
        self.templates = {}
        
        # Load all prompt templates
        self._load_all_templates()
        
        logger.info(f"Prompt Manager initialized with {len(self.templates)} templates")
    
    def _load_all_templates(self) -> None:
        """Load all prompt templates from the prompts directory."""
        template_files = list(self.prompts_dir.glob("*.json"))
        
        for template_file in template_files:
            agent_id = template_file.stem
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)
                
                self.templates[agent_id] = template_data
                logger.info(f"Loaded prompt template for {agent_id}")
            except Exception as e:
                logger.error(f"Error loading prompt template {template_file}: {str(e)}")
    
    def get_prompt(self, agent_id: str, prompt_type: str, **kwargs) -> str:
        """Get a formatted prompt for a specific agent and task.
        
        Args:
            agent_id: The ID of the agent (e.g., "SAA", "RAA")
            prompt_type: The type of prompt (e.g., "task_execution", "query_processing")
            **kwargs: Variables to format the prompt template with
            
        Returns:
            Formatted prompt string
        """
        if agent_id not in self.templates:
            logger.warning(f"No prompt templates found for agent {agent_id}")
            return f"You are the {agent_id} agent. Please complete the task: {prompt_type}"
        
        if prompt_type not in self.templates[agent_id]:
            logger.warning(f"No {prompt_type} prompt found for agent {agent_id}")
            return f"You are the {agent_id} agent. Please complete the task: {prompt_type}"
        
        # Get the prompt template
        template = self.templates[agent_id][prompt_type]
        
        # Create the complete prompt by combining sections
        prompt_parts = []
        
        # Add role description
        if "role" in template:
            prompt_parts.append(f"# Role\n{template['role']}")
        
        # Add task description
        if "task" in template:
            prompt_parts.append(f"# Task\n{template['task']}")
        
        # Add guidelines
        if "guidelines" in template:
            prompt_parts.append(f"# Guidelines\n{template['guidelines']}")
        
        # Add input description
        if "input_description" in template:
            prompt_parts.append(f"# Input\n{template['input_description']}")
        
        # Add expected output format
        if "output_format" in template:
            prompt_parts.append(f"# Expected Output Format\n{template['output_format']}")
        
        # Add examples if available
        if "examples" in template:
            examples_text = "# Examples\n"
            for example in template["examples"]:
                examples_text += f"\n## Example Input\n{example['input']}\n\n## Example Output\n{example['output']}\n"
            prompt_parts.append(examples_text)
        
        # Combine all parts
        complete_prompt = "\n\n".join(prompt_parts)
        
        # Format the prompt with the provided variables
        try:
            formatted_prompt = complete_prompt.format(**kwargs)
            return formatted_prompt
        except KeyError as e:
            logger.error(f"Missing key in prompt formatting: {str(e)}")
            # Return unformatted prompt as fallback
            return complete_prompt
    
    def save_template(self, agent_id: str, template_data: Dict[str, Any]) -> bool:
        """Save a new or updated prompt template.
        
        Args:
            agent_id: The ID of the agent
            template_data: The template data to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            template_path = self.prompts_dir / f"{agent_id}.json"
            with open(template_path, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, indent=2)
            
            # Update in-memory template
            self.templates[agent_id] = template_data
            
            logger.info(f"Saved prompt template for {agent_id}")
            return True
        except Exception as e:
            logger.error(f"Error saving prompt template for {agent_id}: {str(e)}")
            return False
    
    def get_template(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get the raw template for an agent.
        
        Args:
            agent_id: The ID of the agent
            
        Returns:
            Template dictionary or None if not found
        """
        return self.templates.get(agent_id)