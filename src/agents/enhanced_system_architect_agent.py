"""
Enhanced System Architect Agent for Domain-SC.

This agent uses simulation-based approaches to generate more consistent
and cost-effective architecture designs.
"""

import os
import logging
import json
import hashlib
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

from agents.base_agent import BaseAgent
from utils.logger import setup_logger
from services.optimized_llm_service import OptimizedLLMService
from services.enhanced_rag_service import EnhancedRAGService
from prompts.adaptive_prompt_system import AdaptivePromptSystem

logger = setup_logger(__name__, "system_architect_agent.log")

class EnhancedSystemArchitectAgent(BaseAgent):
    """Enhanced System Architect Agent with simulation capabilities."""
    
    def __init__(self, agent_id: str = "SAA", name: str = "System Architect Agent"):
        """Initialize the enhanced system architect agent."""
        super().__init__(agent_id, name)
        
        # Use optimized services
        self.llm_service = OptimizedLLMService()
        self.rag_service = EnhancedRAGService(llm_service=self.llm_service)
        self.prompt_system = AdaptivePromptSystem()
        
        # Design cache to avoid regenerating similar designs
        self.design_cache = {}
        
        logger.info(f"Enhanced System Architect Agent {agent_id} initialized")
    
    def _decompose_task(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decompose a complex architecture task into subtasks."""
        # Define subtasks based on task type
        task_type = task.get("type", "architecture_design")
        
        if task_type == "architecture_design":
            requirements = task.get("requirements", {})
            constraints = task.get("constraints", {})
            
            subtasks = [
                {
                    "type": "pattern_selection",
                    "description": "Select appropriate architecture patterns",
                    "requirements": requirements,
                    "constraints": constraints
                },
                {
                    "type": "component_identification",
                    "description": "Identify key system components",
                    "requirements": requirements,
                    "constraints": constraints
                },
                {
                    "type": "interface_design",
                    "description": "Design component interfaces",
                    "requirements": requirements,
                    "constraints": constraints
                },
                {
                    "type": "data_flow_mapping",
                    "description": "Map data flows between components",
                    "requirements": requirements,
                    "constraints": constraints
                }
            ]
            return subtasks
        else:
            # For simple tasks, just return the original
            return [task]
    
    def _simulate_subtask(self, subtask: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate expected outcome for a subtask."""
        task_type = subtask.get("type")
        
        # Create simulation prompt
        template = self.prompt_system.get_prompt_template(self.agent_id, f"simulate_{task_type}")
        
        if not template:
            logger.warning(f"No simulation template found for {task_type}")
            # Create a more generic simulation
            return self._simulate_generic(subtask)
            
        # Format prompt with subtask details
        simulation_prompt = self.prompt_system.format_prompt(
            template,
            task_description=subtask.get("description", ""),
            requirements=json.dumps(subtask.get("requirements", {}), indent=2),
            constraints=json.dumps(subtask.get("constraints", {}), indent=2)
        )
        
        # Execute simulation with lightweight model
        simulation_response = self.llm_service.generate_text(
            prompt=simulation_prompt,
            model="gpt-3.5-turbo" if "gpt" in self.llm_service.model else "claude-3-haiku",
            temperature=0.1,  # Lower temperature for more deterministic output
            use_cache=True,
            task_complexity="low"
        )
        
        # Parse simulation result
        try:
            # Attempt to extract JSON
            result_start = simulation_response.find("{")
            result_end = simulation_response.rfind("}") + 1
            
            if result_start >= 0 and result_end > result_start:
                result_json = simulation_response[result_start:result_end]
                return json.loads(result_json)
            else:
                # If no JSON found, return structured summary
                return {
                    "status": "success",
                    "simulation": simulation_response,
                    "task_type": task_type
                }
        except Exception as e:
            logger.warning(f"Error parsing simulation result: {str(e)}")
            return {
                "status": "partial",
                "simulation": simulation_response,
                "task_type": task_type
            }
    
    def _simulate_generic(self, subtask: Dict[str, Any]) -> Dict[str, Any]:
        """Generic simulation for subtasks without specific simulation templates."""
        task_type = subtask.get("type")
        
        # Generic simulation prompt
        simulation_prompt = f"""You are simulating the expected output of a system architecture task.

TASK TYPE: {task_type}
DESCRIPTION: {subtask.get('description', '')}

REQUIREMENTS:
{json.dumps(subtask.get('requirements', {}), indent=2)}

CONSTRAINTS:
{json.dumps(subtask.get('constraints', {}), indent=2)}

Return a prediction of what would be the expected output structure for this task.
Your output should be in JSON format with at least these fields:
- expected_keys: List of keys that should be in the result
- status: "success" or "error"
- typical_patterns: List of typical patterns for this type of task (if applicable)

Output ONLY the JSON and nothing else.
"""
        
        # Execute simulation
        simulation_response = self.llm_service.generate_text(
            prompt=simulation_prompt,
            model="gpt-3.5-turbo" if "gpt" in self.llm_service.model else "claude-3-haiku",
            temperature=0.1,
            use_cache=True,
            task_complexity="low"
        )
        
        # Parse result
        try:
            result_start = simulation_response.find("{")
            result_end = simulation_response.rfind("}") + 1
            
            if result_start >= 0 and result_end > result_start:
                result_json = simulation_response[result_start:result_end]
                return json.loads(result_json)
            else:
                # No JSON found
                return {
                    "status": "partial",
                    "simulation": simulation_response,
                    "task_type": task_type,
                    "expected_keys": ["status", "result"]
                }
        except Exception as e:
            logger.warning(f"Error parsing generic simulation: {str(e)}")
            return {
                "status": "partial",
                "simulation": simulation_response,
                "task_type": task_type,
                "expected_keys": ["status", "result"]
            }
    
    def _execute_subtask(self, subtask: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a subtask with the full system."""
        task_type = subtask.get("type")
        
        # Get prompt template
        template = self.prompt_system.get_prompt_template(self.agent_id, task_type)
        
        if not template:
            logger.warning(f"No template found for {task_type}")
            return {"status": "error", "message": f"No template for {task_type}"}
        
        # Get RAG context for the task
        query = f"{subtask.get('description')} for {json.dumps(subtask.get('requirements', {}))}"
        rag_context = self.rag_service.retrieve_for_query(query)
        
        # Format prompt with subtask details and RAG context
        context_text = "\n\n".join([doc.get("document", "") for doc in rag_context])
        
        execution_prompt = self.prompt_system.format_prompt(
            template,
            task_description=subtask.get("description", ""),
            requirements=json.dumps(subtask.get("requirements", {}), indent=2),
            constraints=json.dumps(subtask.get("constraints", {}), indent=2),
            context=context_text
        )
        
        # Execute task with full model
        execution_response = self.llm_service.generate_text(
            prompt=execution_prompt,
            temperature=0.2,
            use_cache=True,
            task_complexity="medium"
        )
        
        # Parse result
        try:
            # Try to extract structured data
            # Patterns for common JSON/YAML blocks in response
            json_start = execution_response.find("```json")
            json_end = execution_response.find("```", json_start + 6) if json_start >= 0 else -1
            
            if json_start >= 0 and json_end > json_start:
                json_block = execution_response[json_start + 7:json_end].strip()
                result_data = json.loads(json_block)
                return {
                    "status": "success",
                    "result": result_data,
                    "task_type": task_type,
                    "raw_response": execution_response
                }
            else:
                # If no structured data, return the raw response
                return {
                    "status": "success",
                    "result": execution_response,
                    "task_type": task_type
                }
        except Exception as e:
            logger.warning(f"Error parsing execution result: {str(e)}")
            return {
                "status": "partial",
                "result": execution_response,
                "task_type": task_type
            }
    
    def _significant_deviation(self, actual: Dict[str, Any], expected: Dict[str, Any]) -> bool:
        """Check if actual result significantly deviates from expected simulation."""
        # If either result has error status, that's a significant deviation
        if actual.get("status") == "error" or expected.get("status") == "error":
            return True
            
        # Compare task types
        if actual.get("task_type") != expected.get("task_type"):
            return True
            
        # For structured results, do more detailed comparison
        if "result" in actual and isinstance(actual["result"], dict):
            # Check for missing key sections
            expected_keys = expected.get("expected_keys", [])
            if expected_keys:
                actual_keys = set(actual["result"].keys() if isinstance(actual["result"], dict) else [])
                missing_keys = [k for k in expected_keys if k not in actual_keys]
                if missing_keys:
                    logger.warning(f"Missing expected sections: {missing_keys}")
                    return True
        
        return False
    
    def _execute_with_guidance(self, subtask: Dict[str, Any], expected: Dict[str, Any]) -> Dict[str, Any]:
        """Execute subtask with guidance from simulation."""
        task_type = subtask.get("type")
        
        # Get guided execution template
        template = self.prompt_system.get_prompt_template(self.agent_id, f"guided_{task_type}")
        
        if not template:
            logger.warning(f"No guided template found for {task_type}, falling back to regular template")
            template = self.prompt_system.get_prompt_template(self.agent_id, task_type)
            
        if not template:
            logger.warning(f"No template found for {task_type}")
            return {"status": "error", "message": f"No template for {task_type}"}
        
        # Get RAG context for the task
        query = f"{subtask.get('description')} for {json.dumps(subtask.get('requirements', {}))}"
        rag_context = self.rag_service.retrieve_for_query(query)
        
        # Format prompt with subtask details, RAG context, and simulation guidance
        context_text = "\n\n".join([doc.get("document", "") for doc in rag_context])
        expected_result = expected.get("simulation", "") or json.dumps(expected, indent=2)
        
        guided_prompt = self.prompt_system.format_prompt(
            template,
            task_description=subtask.get("description", ""),
            requirements=json.dumps(subtask.get("requirements", {}), indent=2),
            constraints=json.dumps(subtask.get("constraints", {}), indent=2),
            context=context_text,
            expected_outcome=expected_result
        )
        
        # Execute task with guided prompt
        guided_response = self.llm_service.generate_text(
            prompt=guided_prompt,
            temperature=0.1,  # Lower temperature for guided execution
            use_cache=False,  # Don't use cache for guided execution
            task_complexity="high"  # Higher complexity due to additional guidance
        )
        
        # Parse result similar to _execute_subtask
        try:
            json_start = guided_response.find("```json")
            json_end = guided_response.find("```", json_start + 6) if json_start >= 0 else -1
            
            if json_start >= 0 and json_end > json_start:
                json_block = guided_response[json_start + 7:json_end].strip()
                result_data = json.loads(json_block)
                return {
                    "status": "success",
                    "result": result_data,
                    "task_type": task_type,
                    "guided": True,
                    "raw_response": guided_response
                }
            else:
                return {
                    "status": "success",
                    "result": guided_response,
                    "task_type": task_type,
                    "guided": True
                }
        except Exception as e:
            logger.warning(f"Error parsing guided execution result: {str(e)}")
            return {
                "status": "partial",
                "result": guided_response,
                "task_type": task_type,
                "guided": True
            }
    
    def _synthesize_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Synthesize results from subtasks into a coherent architecture."""
        # Create synthesis prompt
        template = self.prompt_system.get_prompt_template(self.agent_id, "synthesize_architecture")
        
        if not template:
            logger.warning("No synthesis template found")
            # Create basic synthesis by combining results
            synthesis = {
                "components": [],
                "interfaces": [],
                "data_flows": [],
                "patterns": []
            }
            
            for result in results:
                if result.get("status") == "success" and isinstance(result.get("result"), dict):
                    for key, value in result["result"].items():
                        if key in synthesis and isinstance(value, list):
                            synthesis[key].extend(value)
            
            return {
                "status": "success",
                "architecture": synthesis
            }
        
        # Format synthesis prompt
        results_text = json.dumps(results, indent=2)
        synthesis_prompt = self.prompt_system.format_prompt(
            template,
            results=results_text
        )
        
        # Execute synthesis
        synthesis_response = self.llm_service.generate_text(
            prompt=synthesis_prompt,
            temperature=0.2,
            task_complexity="high"
        )
        
        # Parse result
        try:
            # Try to extract JSON architecture
            json_start = synthesis_response.find("```json")
            json_end = synthesis_response.find("```", json_start + 6) if json_start >= 0 else -1
            
            if json_start >= 0 and json_end > json_start:
                json_block = synthesis_response[json_start + 7:json_end].strip()
                architecture = json.loads(json_block)
                return {
                    "status": "success",
                    "architecture": architecture,
                    "raw_synthesis": synthesis_response
                }
            else:
                # No structured data found
                return {
                    "status": "success",
                    "architecture": synthesis_response
                }
        except Exception as e:
            logger.warning(f"Error parsing synthesis result: {str(e)}")
            return {
                "status": "partial",
                "architecture": synthesis_response
            }
    
    def _validate_design(self, design: Dict[str, Any], requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Validate design completeness and coherence."""
        # Create validation prompt
        template = self.prompt_system.get_prompt_template(self.agent_id, "validate_architecture")
        
        if not template:
            logger.warning("No validation template found")
            return {"complete": True, "gaps": []}
            
        # Format validation prompt
        design_json = json.dumps(design, indent=2)
        requirements_json = json.dumps(requirements, indent=2)
        
        validation_prompt = self.prompt_system.format_prompt(
            template,
            design=design_json,
            requirements=requirements_json
        )
        
        # Execute validation
        validation_response = self.llm_service.generate_text(
            prompt=validation_prompt,
            temperature=0.1,
            task_complexity="medium"
        )
        
        # Parse validation result
        try:
            # Try to extract structured data
            json_start = validation_response.find("```json")
            json_end = validation_response.find("```", json_start + 6) if json_start >= 0 else -1
            
            if json_start >= 0 and json_end > json_start:
                json_block = validation_response[json_start + 7:json_end].strip()
                validation_result = json.loads(json_block)
                return validation_result
            
            # Try to infer completeness from text
            if "incomplete" in validation_response.lower() or "missing" in validation_response.lower():
                # Extract gaps as list items
                gaps = []
                lines = validation_response.split("\n")
                for line in lines:
                    if line.strip().startswith(("- ", "* ", "• ")):
                        gaps.append(line.strip()[2:])
                
                return {
                    "complete": False,
                    "gaps": gaps,
                    "raw_validation": validation_response
                }
            else:
                return {
                    "complete": True,
                    "gaps": [],
                    "raw_validation": validation_response
                }
        except Exception as e:
            logger.warning(f"Error parsing validation result: {str(e)}")
            return {
                "complete": False,
                "gaps": ["Error validating design"],
                "raw_validation": validation_response
            }
    
    def _address_gaps(self, design: Dict[str, Any], gaps: List[str]) -> Dict[str, Any]:
        """Address gaps in the design."""
        # Create gap-filling prompt
        template = self.prompt_system.get_prompt_template(self.agent_id, "address_gaps")
        
        if not template:
            logger.warning("No gap-addressing template found")
            return design
            
        # Format gap-filling prompt
        design_json = json.dumps(design, indent=2)
        gaps_json = json.dumps(gaps, indent=2)
        
        gap_prompt = self.prompt_system.format_prompt(
            template,
            design=design_json,
            gaps=gaps_json
        )
        
        # Execute gap filling
        gap_response = self.llm_service.generate_text(
            prompt=gap_prompt,
            temperature=0.3,
            task_complexity="high"
        )
        
        # Parse result
        try:
            # Try to extract enhanced design
            json_start = gap_response.find("```json")
            json_end = gap_response.find("```", json_start + 6) if json_start >= 0 else -1
            
            if json_start >= 0 and json_end > json_start:
                json_block = gap_response[json_start + 7:json_end].strip()
                enhanced_design = json.loads(json_block)
                return enhanced_design
            else:
                # No structured design found, return original with warning
                logger.warning("Gap addressing didn't return structured design")
                return design
        except Exception as e:
            logger.warning(f"Error parsing gap-filled design: {str(e)}")
            return design
    
    def design_architecture(self, requirements: Dict[str, Any], constraints: Dict[str, Any] = None) -> Dict[str, Any]:
        """Design architecture with simulation and validation."""
        # Create cache key for this design request
        requirements_str = json.dumps(requirements, sort_keys=True)
        constraints_str = json.dumps(constraints or {}, sort_keys=True)
        cache_key = hashlib.md5((requirements_str + constraints_str).encode()).hexdigest()
        
        # Check cache
        if cache_key in self.design_cache:
            logger.info("Using cached architecture design")
            return self.design_cache[cache_key]
            
        # Create task for architecture design
        task = {
            "type": "architecture_design",
            "requirements": requirements,
            "constraints": constraints or {}
        }
        
        # Break down into subtasks
        subtasks = self._decompose_task(task)
        
        # Plan execution with simulation
        execution_plan = []
        for subtask in subtasks:
            # Simulate expected output
            expected_output = self._simulate_subtask(subtask)
            execution_plan.append((subtask, expected_output))
            
        # Execute subtasks with validation against simulations
        results = []
        for subtask, expected in execution_plan:
            # Execute the subtask
            actual = self._execute_subtask(subtask)
            
            # Check if result matches expectation
            if self._significant_deviation(actual, expected):
                logger.warning(f"Significant deviation in {subtask['type']} - re-running with guidance")
                # Re-run with guidance
                actual = self._execute_with_guidance(subtask, expected)
                
            results.append(actual)
            
        # Synthesize subtask results
        design = self._synthesize_results(results)
        
        # Get the architecture from synthesis result
        architecture = (design.get("architecture", {}) 
                      if isinstance(design.get("architecture"), dict) 
                      else {"raw_design": design.get("architecture", "")})
        
        # Validate design completeness
        validation_results = self._validate_design(architecture, requirements)
        
        # Address gaps if found
        if not validation_results.get("complete", True):
            gaps = validation_results.get("gaps", [])
            logger.info(f"Addressing {len(gaps)} gaps in design")
            architecture = self._address_gaps(architecture, gaps)
            
        # Add metadata
        final_design = {
            "architecture": architecture,
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "agent_id": self.agent_id,
                "requirements_hash": cache_key[:8]
            }
        }
        
        # Cache the result
        self.design_cache[cache_key] = final_design
        
        return final_design
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task based on its type."""
        task_type = task.get("type", "")
        
        if task_type == "architecture_design":
            return self.design_architecture(
                task.get("requirements", {}),
                task.get("constraints", {})
            )
        else:
            logger.warning(f"Unknown task type: {task_type}")
            return {"status": "error", "message": f"Unknown task type: {task_type}"}