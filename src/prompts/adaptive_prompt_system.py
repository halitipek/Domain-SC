"""
Adaptive Prompt System for Domain-SC.

This system manages prompt templates with performance tracking and selection,
enabling automatic optimization of prompts for different tasks.
"""

import os
import json
import yaml
import logging
import hashlib
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import random

from src.utils.logger import setup_logger

logger = setup_logger(__name__, "prompt_system.log")

class AdaptivePromptSystem:
    """System for managing and optimizing prompt templates."""
    
    def __init__(self, template_dir: str = None):
        """Initialize the adaptive prompt system."""
        self.template_dir = template_dir or os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
            "src", "prompts", "templates", "enhanced"
        )
        
        # Ensure the template directory exists
        os.makedirs(self.template_dir, exist_ok=True)
        
        # Also check standard template directory for fallback
        self.standard_template_dir = os.path.join(
            os.path.dirname(self.template_dir), 
        )
        
        # Load templates from directory
        self.templates = self._load_templates()
        
        # Performance metrics storage
        self.performance_metrics_file = os.path.join(self.template_dir, "performance_metrics.json")
        self.performance_metrics = self._load_performance_metrics()
        
        # Template version tracking
        self.template_versions = self._load_template_versions()
        
        logger.info(f"Adaptive Prompt System initialized with {len(self.templates)} templates")
    
    def _load_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load prompt templates from directory."""
        templates = {}
        
        # Load enhanced templates first
        if os.path.exists(self.template_dir):
            for filename in os.listdir(self.template_dir):
                if filename.endswith(('.yaml', '.yml', '.json')) and not filename.startswith('.'):
                    try:
                        file_path = os.path.join(self.template_dir, filename)
                        template_id = os.path.splitext(filename)[0]
                        
                        if filename.endswith(('.yaml', '.yml')):
                            with open(file_path, 'r') as f:
                                template_data = yaml.safe_load(f)
                        else:
                            with open(file_path, 'r') as f:
                                template_data = json.load(f)
                        
                        # Validate template
                        if self._validate_template(template_data):
                            templates[template_id] = template_data
                            logger.info(f"Loaded enhanced template: {template_id}")
                        else:
                            logger.warning(f"Invalid template format: {template_id}")
                            
                    except Exception as e:
                        logger.error(f"Error loading template {filename}: {str(e)}")
        
        # Load standard templates as fallback
        if os.path.exists(self.standard_template_dir):
            for filename in os.listdir(self.standard_template_dir):
                if filename.endswith(('.yaml', '.yml', '.json')) and not filename.startswith('.'):
                    try:
                        file_path = os.path.join(self.standard_template_dir, filename)
                        template_id = os.path.splitext(filename)[0]
                        
                        # Skip if already loaded in enhanced templates
                        if template_id in templates:
                            continue
                            
                        if filename.endswith(('.yaml', '.yml')):
                            with open(file_path, 'r') as f:
                                template_data = yaml.safe_load(f)
                        else:
                            with open(file_path, 'r') as f:
                                template_data = json.load(f)
                        
                        # Validate template
                        if self._validate_template(template_data):
                            templates[template_id] = template_data
                            logger.info(f"Loaded standard template: {template_id}")
                        else:
                            logger.warning(f"Invalid template format: {template_id}")
                            
                    except Exception as e:
                        logger.error(f"Error loading template {filename}: {str(e)}")
        
        # If no templates found, create example templates
        if not templates:
            logger.warning("No templates found. Creating example templates.")
            templates = self._create_example_templates()
            
        return templates
    
    def _create_example_templates(self) -> Dict[str, Dict[str, Any]]:
        """Create example templates for the system to function."""
        templates = {}
        
        # Create a simple simulation template
        simulation_template = {
            "agent_id": "SAA",
            "prompt_type": "simulate_pattern_selection",
            "version": "1.0.0",
            "template": """You are the System Architect Agent's simulation module.

TASK: Predict the appropriate architecture patterns for the following requirements and constraints.

REQUIREMENTS:
{requirements}

CONSTRAINTS:
{constraints}

INSTRUCTIONS:
1. Analyze the requirements and constraints.
2. Predict which architecture patterns would be most suitable.
3. Return your prediction in JSON format with the following structure:
   - patterns: array of pattern names
   - justifications: object mapping each pattern to justification
   - expected_keys: array of expected keys in the final output

Output ONLY the JSON object and nothing else.
"""
        }
        
        # Create an execution template
        execution_template = {
            "agent_id": "SAA",
            "prompt_type": "pattern_selection",
            "version": "1.0.0",
            "template": """You are the System Architect Agent responsible for selecting architecture patterns.

TASK: Select the most appropriate architecture patterns for the following requirements and constraints.

REQUIREMENTS:
{requirements}

CONSTRAINTS:
{constraints}

RELEVANT CONTEXT:
{context}

INSTRUCTIONS:
1. Analyze the requirements and constraints thoroughly.
2. Select the most appropriate architecture patterns.
3. Provide detailed justification for each selected pattern.
4. Return your selection in JSON format with the following structure:
   - patterns: array of pattern names
   - justifications: object mapping each pattern to justification
   - alternatives: array of alternative patterns that were considered

Output the JSON object wrapped in ```json and ``` tags.
"""
        }
        
        # Save templates
        template_id1 = self.add_new_template_version(simulation_template)
        template_id2 = self.add_new_template_version(execution_template)
        
        # Add to templates dict
        templates[template_id1] = simulation_template
        templates[template_id2] = execution_template
        
        return templates
    
    def _validate_template(self, template_data: Dict[str, Any]) -> bool:
        """Validate that a template has the required fields."""
        required_fields = ["agent_id", "prompt_type", "template"]
        if not all(field in template_data for field in required_fields):
            return False
        
        # Ensure version field exists
        if "version" not in template_data:
            template_data["version"] = "1.0.0"
            
        return True
    
    def _load_performance_metrics(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load performance metrics for templates."""
        if os.path.exists(self.performance_metrics_file):
            try:
                with open(self.performance_metrics_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading performance metrics: {str(e)}")
                return {}
        return {}
    
    def _save_performance_metrics(self):
        """Save performance metrics to file."""
        try:
            with open(self.performance_metrics_file, 'w') as f:
                json.dump(self.performance_metrics, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving performance metrics: {str(e)}")
    
    def _load_template_versions(self) -> Dict[str, str]:
        """Load template version information."""
        versions = {}
        for template_id, template in self.templates.items():
            versions[template_id] = template.get("version", "1.0.0")
        return versions
    
    def get_prompt_template(self, agent_id: str, prompt_type: str) -> Optional[Dict[str, Any]]:
        """Get the best template for a given agent and prompt type."""
        # Find all matching templates
        matching_templates = {}
        for template_id, template in self.templates.items():
            if (template.get("agent_id") == agent_id and 
                template.get("prompt_type") == prompt_type):
                matching_templates[template_id] = template
        
        if not matching_templates:
            logger.warning(f"No templates found for agent_id={agent_id}, prompt_type={prompt_type}")
            return None
        
        # If only one template, return it
        if len(matching_templates) == 1:
            return list(matching_templates.values())[0]
        
        # Select best template based on performance
        return self._select_best_template(list(matching_templates.keys()))
    
    def _select_best_template(self, template_ids: List[str]) -> Dict[str, Any]:
        """Select the best template based on historical performance."""
        # Calculate average performance score for each template
        template_scores = {}
        for template_id in template_ids:
            metrics = self.performance_metrics.get(template_id, [])
            if not metrics:
                template_scores[template_id] = 0.5  # Default for new templates
                continue
                
            # Calculate average score from last 20 uses
            recent_metrics = metrics[-20:]
            avg_score = sum(m.get("score", 0) for m in recent_metrics) / len(recent_metrics)
            template_scores[template_id] = avg_score
        
        # Add exploration factor (epsilon-greedy approach)
        exploration_rate = 0.1  # 10% random exploration
        if random.random() < exploration_rate:
            # Randomly select template for exploration
            selected_id = random.choice(template_ids)
            logger.info(f"Exploring random template: {selected_id}")
        else:
            # Select highest scoring template
            selected_id = max(template_scores, key=template_scores.get)
            logger.info(f"Selected best template: {selected_id} (score: {template_scores[selected_id]:.2f})")
        
        return self.templates[selected_id]
    
    def format_prompt(self, template: Dict[str, Any], **kwargs) -> str:
        """Format a prompt template with provided variables."""
        template_str = template.get("template", "")
        
        # Simple string formatting
        try:
            formatted = template_str.format(**kwargs)
            return formatted
        except KeyError as e:
            logger.error(f"Missing variable in template: {str(e)}")
            # Fall back to partial formatting
            for key, value in kwargs.items():
                template_str = template_str.replace(f"{{{key}}}", str(value))
            return template_str
    
    def update_template_performance(self, agent_id: str, prompt_type: str, score: float, metadata: Dict[str, Any] = None):
        """Update performance metrics for a template."""
        # Find the template ID
        template_id = None
        for tid, template in self.templates.items():
            if (template.get("agent_id") == agent_id and 
                template.get("prompt_type") == prompt_type):
                template_id = tid
                break
        
        if not template_id:
            logger.warning(f"No template found for agent_id={agent_id}, prompt_type={prompt_type}")
            return
        
        # Add performance record
        if template_id not in self.performance_metrics:
            self.performance_metrics[template_id] = []
        
        performance_record = {
            "timestamp": datetime.now().isoformat(),
            "score": max(0, min(score, 1)),  # Clamp to 0-1
            "version": self.template_versions.get(template_id, "1.0.0")
        }
        
        # Add metadata if provided
        if metadata:
            performance_record["metadata"] = metadata
        
        self.performance_metrics[template_id].append(performance_record)
        
        # Save metrics
        self._save_performance_metrics()
        logger.info(f"Updated performance metrics for template {template_id} with score {score:.2f}")
    
    def add_new_template_version(self, template_data: Dict[str, Any]) -> str:
        """Add a new template version."""
        # Validate template data
        if not self._validate_template(template_data):
            logger.error("Invalid template format")
            return "error: invalid template format"
            
        agent_id = template_data.get("agent_id")
        prompt_type = template_data.get("prompt_type")
        
        # Find existing template for same agent/prompt type
        existing_id = None
        for tid, template in self.templates.items():
            if (template.get("agent_id") == agent_id and 
                template.get("prompt_type") == prompt_type):
                existing_id = tid
                break
        
        # Create template ID
        if existing_id:
            # Increment version
            current_version = self.template_versions.get(existing_id, "1.0.0")
            version_parts = current_version.split(".")
            new_version = f"{version_parts[0]}.{version_parts[1]}.{int(version_parts[2]) + 1}"
            template_data["version"] = new_version
            
            # Use same template ID but update version
            template_id = existing_id
            self.template_versions[template_id] = new_version
        else:
            # Create new template ID
            template_id = f"{agent_id}_{prompt_type}".lower()
            template_data["version"] = "1.0.0"
            self.template_versions[template_id] = "1.0.0"
        
        # Save template
        self.templates[template_id] = template_data
        
        # Save to file
        try:
            file_path = os.path.join(self.template_dir, f"{template_id}.yaml")
            with open(file_path, 'w') as f:
                yaml.dump(template_data, f, default_flow_style=False)
            logger.info(f"Added/updated template: {template_id} (version: {template_data['version']})")
        except Exception as e:
            logger.error(f"Error saving template: {str(e)}")
        
        return template_id
    
    def get_template_performance_stats(self, template_id: str = None) -> Dict[str, Any]:
        """Get performance statistics for templates."""
        stats = {}
        
        if template_id:
            # Get stats for specific template
            if template_id not in self.performance_metrics:
                return {"error": "Template ID not found"}
                
            metrics = self.performance_metrics[template_id]
            if not metrics:
                return {"count": 0, "avg_score": 0}
                
            avg_score = sum(m.get("score", 0) for m in metrics) / len(metrics)
            stats = {
                "template_id": template_id,
                "count": len(metrics),
                "avg_score": avg_score,
                "version": self.template_versions.get(template_id, "unknown")
            }
        else:
            # Get stats for all templates
            for tid, metrics in self.performance_metrics.items():
                if not metrics:
                    continue
                    
                avg_score = sum(m.get("score", 0) for m in metrics) / len(metrics)
                stats[tid] = {
                    "count": len(metrics),
                    "avg_score": avg_score,
                    "version": self.template_versions.get(tid, "unknown")
                }
        
        return stats