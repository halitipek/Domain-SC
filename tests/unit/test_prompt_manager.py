"""
Unit tests for the prompt manager.
"""

import os
import unittest
import tempfile
from pathlib import Path
import json
import shutil

# Add project root to Python path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.prompts.prompt_manager import PromptManager


class TestPromptManager(unittest.TestCase):
    """Tests for the PromptManager class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for templates
        self.test_dir = tempfile.mkdtemp()
        
        # Create test template files
        self.test_agent_id = "TEST"
        self.test_template_path = os.path.join(self.test_dir, f"{self.test_agent_id}.json")
        
        self.test_template = {
            "role": "You are a test agent.",
            "test_prompt": {
                "role": "You are a test agent.",
                "task": "Your task is to {task_description}.",
                "guidelines": "1. Follow test guidelines.\n2. Be thorough.",
                "input_description": "You have been provided with: {input_description}",
                "output_format": "Your output should follow this format: {output_format}"
            }
        }
        
        with open(self.test_template_path, "w") as f:
            json.dump(self.test_template, f, indent=2)
        
        # Create prompt manager with test directory
        self.prompt_manager = PromptManager(prompts_dir=self.test_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        # Remove test directory and contents
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test initialization of the PromptManager."""
        self.assertEqual(self.prompt_manager.prompts_dir, Path(self.test_dir))
        self.assertIn(self.test_agent_id, self.prompt_manager.templates)
        self.assertEqual(self.prompt_manager.templates[self.test_agent_id], self.test_template)
    
    def test_get_prompt(self):
        """Test getting a formatted prompt."""
        # Test with existing prompt
        prompt = self.prompt_manager.get_prompt(
            agent_id=self.test_agent_id,
            prompt_type="test_prompt",
            task_description="test task",
            input_description="test input",
            output_format="JSON"
        )
        
        # Verify prompt content
        self.assertIn("You are a test agent.", prompt)
        self.assertIn("Your task is to test task.", prompt)
        self.assertIn("You have been provided with: test input", prompt)
        self.assertIn("Your output should follow this format: JSON", prompt)
        
        # Test with nonexistent agent
        fallback_prompt = self.prompt_manager.get_prompt(
            agent_id="NONEXISTENT",
            prompt_type="test_prompt"
        )
        
        # Verify fallback prompt
        self.assertIn("You are the NONEXISTENT agent", fallback_prompt)
        
        # Test with nonexistent prompt type
        fallback_prompt = self.prompt_manager.get_prompt(
            agent_id=self.test_agent_id,
            prompt_type="nonexistent_prompt_type"
        )
        
        # Verify fallback prompt
        self.assertIn("You are the TEST agent", fallback_prompt)
    
    def test_save_template(self):
        """Test saving a template."""
        # Create a new template
        new_agent_id = "NEW"
        new_template = {
            "role": "You are a new agent.",
            "new_prompt": {
                "role": "You are a new agent.",
                "task": "Your task is to perform a new task."
            }
        }
        
        # Save the template
        result = self.prompt_manager.save_template(new_agent_id, new_template)
        
        # Verify result
        self.assertTrue(result)
        
        # Verify template is saved
        self.assertIn(new_agent_id, self.prompt_manager.templates)
        self.assertEqual(self.prompt_manager.templates[new_agent_id], new_template)
        
        # Verify file is created
        new_template_path = os.path.join(self.test_dir, f"{new_agent_id}.json")
        self.assertTrue(os.path.exists(new_template_path))
        
        # Verify file content
        with open(new_template_path, "r") as f:
            loaded_template = json.load(f)
        self.assertEqual(loaded_template, new_template)
    
    def test_get_template(self):
        """Test getting a raw template."""
        # Get existing template
        template = self.prompt_manager.get_template(self.test_agent_id)
        
        # Verify template
        self.assertEqual(template, self.test_template)
        
        # Get nonexistent template
        nonexistent_template = self.prompt_manager.get_template("NONEXISTENT")
        
        # Verify nonexistent template
        self.assertIsNone(nonexistent_template)


if __name__ == "__main__":
    unittest.main()