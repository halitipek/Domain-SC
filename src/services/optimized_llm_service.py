"""
Optimized LLM Service for Domain-SC.
This service enhances LLM interactions with token optimization, smart model selection,
and simulation-based error prevention.
"""

import os
import json
import logging
import time
import re
import hashlib
from typing import Dict, Any, Optional, List, Union
from datetime import datetime

from config.config import LLM_CONFIG
from utils.logger import setup_logger
from dotenv import load_dotenv

logger = setup_logger(__name__, "llm_service.log")

class OptimizedLLMService:
    """Optimized service for managing LLM interactions."""
    
    def __init__(self):
        """Initialize the optimized LLM service."""
        self.config = LLM_CONFIG
        self.model = self.config.get("model", "gpt-4-turbo")
        self.temperature = self.config.get("temperature", 0.2)
        self.top_p = self.config.get("top_p", 0.95)
        self.max_retries = self.config.get("max_retries", 3)
        self.request_timeout = self.config.get("request_timeout", 120)

        # Set up API keys from environment
        load_dotenv()
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
        
        # Initialize API client based on available keys
        self._initialize_client()
        
        # Semantic request cache with advanced caching
        self.cache = {}
        self.cache_ttl = 3600  # 1 hour
        
        # Cost tracking
        self.cost_tracker = {
            "total_tokens": 0,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_cost": 0.0,
            "requests": 0
        }
        
        # Model parameters cache for cost optimization
        self.model_params = self._initialize_model_params()
        
        logger.info(f"Optimized LLM Service initialized with model: {self.model}")
    
    def _initialize_client(self):
        """Initialize the appropriate API client."""
        # Check if OpenAI model and key is available
        if "gpt" in self.model and self.openai_api_key:
            try:
                import openai
                self.client = openai.OpenAI(api_key=self.openai_api_key)
                self.api_type = "openai"
                logger.info("Initialized OpenAI client")
                return
            except ImportError:
                logger.warning("OpenAI package not installed. Install with: pip install openai")
            except Exception as e:
                logger.error(f"Error initializing OpenAI client: {str(e)}")
        
        # Check if Anthropic model and key is available
        if "claude" in self.model and self.anthropic_api_key:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.anthropic_api_key)
                self.api_type = "anthropic"
                logger.info("Initialized Anthropic client")
                return
            except ImportError:
                logger.warning("Anthropic package not installed. Install with: pip install anthropic")
            except Exception as e:
                logger.error(f"Error initializing Anthropic client: {str(e)}")
        
        # If no client could be initialized, warn and use mock implementation
        logger.warning("No LLM API clients could be initialized. Using mock implementation.")
        self.client = None
        self.api_type = "mock"
    
    def _initialize_model_params(self) -> Dict[str, Dict[str, Any]]:
        """Initialize model parameters for cost estimation and token limits."""
        return {
            # OpenAI models
            "gpt-4-turbo": {
                "max_tokens": 128000,
                "input_cost_per_1k": 0.01,
                "output_cost_per_1k": 0.03,
                "tokens_per_word": 1.3
            },
            "gpt-4": {
                "max_tokens": 8192,
                "input_cost_per_1k": 0.03,
                "output_cost_per_1k": 0.06,
                "tokens_per_word": 1.3
            },
            "gpt-3.5-turbo": {
                "max_tokens": 16384,
                "input_cost_per_1k": 0.0015,
                "output_cost_per_1k": 0.002,
                "tokens_per_word": 1.3
            },
            # Anthropic models
            "claude-3-opus": {
                "max_tokens": 200000,
                "input_cost_per_1k": 0.015,
                "output_cost_per_1k": 0.075,
                "tokens_per_word": 1.3
            },
            "claude-3-sonnet": {
                "max_tokens": 200000,
                "input_cost_per_1k": 0.003,
                "output_cost_per_1k": 0.015,
                "tokens_per_word": 1.3
            },
            "claude-3-haiku": {
                "max_tokens": 200000,
                "input_cost_per_1k": 0.00025,
                "output_cost_per_1k": 0.00125,
                "tokens_per_word": 1.3
            }
        }
    
    def _estimate_tokens(self, text: str, model: str = None) -> int:
        """Estimate token count for a text string."""
        if model is None:
            model = self.model
        
        model_params = self.model_params.get(model, {})
        tokens_per_word = model_params.get("tokens_per_word", 1.3)
        
        # Simple estimation based on whitespace
        words = len(text.split())
        return int(words * tokens_per_word)
    
    def _select_optimal_model(self, prompt: str, task_complexity: str = "medium") -> str:
        """Select the optimal model based on prompt and task complexity."""
        # Estimate token count
        estimated_tokens = self._estimate_tokens(prompt)
        
        # Determine task complexity factor
        complexity_factors = {
            "low": 0.5,     # Simple tasks, factual responses
            "medium": 1.0,  # Default complexity
            "high": 1.5     # Complex reasoning, creative tasks
        }
        complexity_factor = complexity_factors.get(task_complexity, 1.0)
        
        # Check if current model is suitable
        current_model_params = self.model_params.get(self.model, {})
        current_model_max_tokens = current_model_params.get("max_tokens", 8192)
        
        # Need at least 3x the estimated tokens for input + output headroom
        required_capacity = estimated_tokens * 3 * complexity_factor
        
        if required_capacity <= current_model_max_tokens * 0.8:
            return self.model  # Current model is suitable
        
        # Select model based on required capacity and complexity
        if self.api_type == "openai":
            if required_capacity > 100000:
                return "gpt-4-turbo"
            elif required_capacity > 32000:
                return "gpt-4-turbo"
            else:
                return "gpt-3.5-turbo" if task_complexity != "high" else "gpt-4-turbo"
        elif self.api_type == "anthropic":
            if required_capacity > 150000 or task_complexity == "high":
                return "claude-3-opus"
            elif required_capacity > 50000 or task_complexity == "medium":
                return "claude-3-sonnet"
            else:
                return "claude-3-haiku"
        
        # Default to original model if no other selection made
        return self.model
    
    def _generate_semantic_cache_key(self, prompt: str, model: str, temperature: float) -> str:
        """Generate a semantic cache key for a request."""
        # Normalize whitespace and remove leading/trailing whitespace
        normalized_prompt = re.sub(r'\s+', ' ', prompt).strip()
        
        # Extract key sections for semantic fingerprinting
        # This focuses on the core query while ignoring formatting instructions
        query_pattern = r'(?:query|question|task|prompt):\s*(.*?)(?:\n|$)'
        core_query = re.search(query_pattern, normalized_prompt, re.IGNORECASE)
        if core_query:
            query_fingerprint = core_query.group(1)
        else:
            # Take the last 50% of the prompt as fingerprint if no query found
            query_fingerprint = normalized_prompt[len(normalized_prompt)//2:]
        
        # Create hash from model parameters and query fingerprint
        hash_input = f"{model}_{temperature:.2f}_{query_fingerprint}"
        return hashlib.md5(hash_input.encode('utf-8')).hexdigest()
    
    def _check_cache(self, prompt: str, model: str, temperature: float) -> Optional[str]:
        """Check if a response is cached."""
        cache_key = self._generate_semantic_cache_key(prompt, model, temperature)
        cached_data = self.cache.get(cache_key)
        
        if cached_data:
            entry_time, response = cached_data
            # Check if the cache entry is still valid
            if (datetime.now().timestamp() - entry_time) < self.cache_ttl:
                logger.info("Cache hit for prompt")
                return response
            else:
                # Remove expired cache entry
                del self.cache[cache_key]
        
        return None
    
    def _update_cache(self, prompt: str, model: str, temperature: float, response: str):
        """Update the cache with a new response."""
        cache_key = self._generate_semantic_cache_key(prompt, model, temperature)
        self.cache[cache_key] = (datetime.now().timestamp(), response)
        
        # Clean up old cache entries
        self._clean_cache()
    
    def _clean_cache(self):
        """Clean up old cache entries."""
        now = datetime.now().timestamp()
        expired_keys = [k for k, v in self.cache.items() if (now - v[0]) > self.cache_ttl]
        for key in expired_keys:
            del self.cache[key]
    
    def _simulate_failure_modes(self, prompt: str) -> Dict[str, float]:
        """Simulate potential failure modes for the prompt."""
        risk_factors = {
            "hallucination_risk": 0.0,
            "ambiguity_risk": 0.0,
            "context_length_risk": 0.0
        }
        
        # Check for hallucination risk factors
        risk_phrases = [
            "latest", "newest", "current", "recent", 
            "today", "now", "present", "modern",
            "specifics about", "details of", "explain exactly how"
        ]
        
        hallucination_count = sum(1 for phrase in risk_phrases if phrase in prompt.lower())
        risk_factors["hallucination_risk"] = min(hallucination_count * 0.1, 0.9)
        
        # Check for ambiguity risk
        if len(prompt.split()) < 15:
            risk_factors["ambiguity_risk"] = 0.7  # Short prompts tend to be ambiguous
        
        # Check for context length risk
        estimated_tokens = self._estimate_tokens(prompt)
        model_params = self.model_params.get(self.model, {})
        max_tokens = model_params.get("max_tokens", 8192)
        risk_factors["context_length_risk"] = min(estimated_tokens / max_tokens * 2, 0.9)
        
        return risk_factors
    
    def _add_factuality_constraints(self, prompt: str) -> str:
        """Add constraints to reduce hallucination risks."""
        constraints = """
IMPORTANT: Only provide information that you're confident is correct. If you're unsure, say "I don't have enough information" rather than guessing. Base your response strictly on facts, not assumptions. If asked about current events or specific details that require updated information, acknowledge the limitations of your knowledge.
"""
        # Add constraints at beginning of prompt
        enhanced_prompt = constraints + "\n\n" + prompt
        return enhanced_prompt
    
    def _validate_output_structure(self, response: str, expected_structure: Optional[List[str]] = None) -> bool:
        """Validate that the output has the expected structure."""
        if not expected_structure:
            return True  # No structure validation needed
            
        # Check if all expected sections are present
        return all(section in response for section in expected_structure)
    
    def _regenerate_with_formatting(self, prompt: str, model: str, temperature: float = None) -> str:
        """Regenerate with explicit formatting instructions."""
        formatting_instruction = """
IMPORTANT: Format your response with clear section headings and structure. Include all of the following sections:
"""
        
        # Extract expected sections from the original prompt
        section_pattern = r'(?:include|provide|write).*?(?:section|heading).*?["\']([^"\']+)["\']'
        expected_sections = re.findall(section_pattern, prompt, re.IGNORECASE)
        
        # If sections found, add them to formatting instruction
        if expected_sections:
            for section in expected_sections:
                formatting_instruction += f"- {section}\n"
        else:
            # Default sections if none found
            formatting_instruction += "- Summary\n- Details\n- Conclusion\n"
        
        # Add formatting instruction to beginning of prompt
        enhanced_prompt = formatting_instruction + "\n\n" + prompt
        
        # Generate with explicit formatting
        return self._generate_with_backoff(enhanced_prompt, model, temperature)
    
    def generate_text(self, 
                     prompt: str, 
                     model: Optional[str] = None, 
                     temperature: Optional[float] = None, 
                     max_tokens: Optional[int] = None,
                     use_cache: bool = True,
                     task_complexity: str = "medium",
                     expected_structure: Optional[List[str]] = None) -> str:
        """Generate text from a prompt with optimized parameters and simulation.
        
        Args:
            prompt: The prompt to send to the LLM
            model: Optional model override
            temperature: Optional temperature override
            max_tokens: Optional max_tokens override
            use_cache: Whether to use the cache
            task_complexity: Complexity level ("low", "medium", "high")
            expected_structure: Optional list of expected section headings
            
        Returns:
            Generated text from the LLM, or error message if generation fails
        """
        if not prompt or not isinstance(prompt, str):
            logger.error(f"Invalid prompt: {type(prompt)}")
            return "Error: Invalid prompt"
            
        # 1. Estimate token usage
        estimated_tokens = self._estimate_tokens(prompt)
        logger.info(f"Estimated prompt tokens: {estimated_tokens}")
        
        # 2. Choose appropriate model based on complexity and token count
        if model is None:
            model = self._select_optimal_model(prompt, task_complexity)
            logger.info(f"Selected model: {model}")
        
        # Use defaults if not provided
        temperature = temperature if temperature is not None else self.temperature
        # Validate temperature is in valid range
        if temperature < 0 or temperature > 1:
            logger.warning(f"Temperature {temperature} outside valid range [0-1], clamping")
            temperature = max(0, min(1, temperature))
        
        max_tokens = max_tokens or 4000
        if max_tokens <= 0:
            logger.warning(f"Invalid max_tokens {max_tokens}, using default")
            max_tokens = 4000
        
        # 3. Check cache if enabled
        if use_cache:
            cached_response = self._check_cache(prompt, model, temperature)
            if cached_response:
                return cached_response
        
        # 4. Simulate failure modes
        risk_factors = self._simulate_failure_modes(prompt)
        enhanced_prompt = prompt
        
        if risk_factors["hallucination_risk"] > 0.7:
            # Add guardrails if high risk detected
            enhanced_prompt = self._add_factuality_constraints(prompt)
            logger.info(f"Added factuality constraints due to high hallucination risk: {risk_factors['hallucination_risk']:.2f}")
        
        # 5. Generate with optimized parameters and backoff
        response = self._generate_with_backoff(enhanced_prompt, model, temperature, max_tokens)
        
        # 6. Validate output structure
        if expected_structure and not self._validate_output_structure(response, expected_structure):
            logger.warning("Output structure validation failed, regenerating with formatting")
            response = self._regenerate_with_formatting(enhanced_prompt, model, temperature)
        
        # 7. Cache the successful response if caching is enabled
        if use_cache and response:
            self._update_cache(prompt, model, temperature, response)
        
        return response
    
    def _generate_with_backoff(self, prompt: str, model: str, temperature: float = None, max_tokens: int = None) -> str:
        """Generate text with exponential backoff retry logic."""
        temperature = temperature if temperature is not None else self.temperature
        max_tokens = max_tokens or 4000
        
        retries = 0
        last_error = None
        
        while retries <= self.max_retries:
            try:
                if not self.client and self.api_type != "mock":
                    logger.warning("No API client available, falling back to mock implementation")
                    response = self._generate_mock(prompt, model, temperature, max_tokens)
                elif self.api_type == "openai":
                    response = self._generate_openai(prompt, model, temperature, max_tokens)
                elif self.api_type == "anthropic":
                    response = self._generate_anthropic(prompt, model, temperature, max_tokens)
                else:
                    # Mock implementation
                    response = self._generate_mock(prompt, model, temperature, max_tokens)
                
                # Verify response is a string
                if not isinstance(response, str):
                    logger.warning(f"Response is not a string: {type(response)}")
                    response = str(response)
                
                return response
                
            except Exception as e:
                last_error = e
                retries += 1
                logger.error(f"Error generating text (retry {retries}/{self.max_retries}): {str(e)}")
                if retries <= self.max_retries:
                    # Exponential backoff
                    wait_time = 2 ** retries
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logger.error("Max retries exceeded")
                    error_msg = f"Error generating response after {self.max_retries} retries: {str(e)}"
                    # Fall back to mock if all retries fail
                    try:
                        mock_fallback = self._generate_mock(prompt, model, temperature, max_tokens)
                        return f"{error_msg}\n\nFallback response: {mock_fallback}"
                    except Exception:
                        return error_msg
    
    def _generate_openai(self, prompt: str, model: str, temperature: float, max_tokens: int) -> str:
        """Generate text using OpenAI API with usage tracking."""
        if not self.client:
            return "OpenAI client not initialized"
        
        messages = [{"role": "user", "content": prompt}]
        
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=self.top_p,
            timeout=self.request_timeout
        )
        
        # Track usage
        usage = completion.usage
        self.cost_tracker["prompt_tokens"] += usage.prompt_tokens
        self.cost_tracker["completion_tokens"] += usage.completion_tokens
        self.cost_tracker["total_tokens"] += usage.total_tokens
        self.cost_tracker["requests"] += 1
        
        # Calculate cost
        model_params = self.model_params.get(model, {})
        input_cost = (usage.prompt_tokens / 1000) * model_params.get("input_cost_per_1k", 0.01)
        output_cost = (usage.completion_tokens / 1000) * model_params.get("output_cost_per_1k", 0.03)
        request_cost = input_cost + output_cost
        self.cost_tracker["total_cost"] += request_cost
        
        logger.info(f"Request cost: ${request_cost:.4f}, Total cost: ${self.cost_tracker['total_cost']:.4f}")
        
        return completion.choices[0].message.content
    
    def _generate_anthropic(self, prompt: str, model: str, temperature: float, max_tokens: int) -> str:
        """Generate text using Anthropic API with usage tracking."""
        if not self.client:
            return "Anthropic client not initialized"
        
        completion = self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Track usage (estimated for Anthropic)
        prompt_tokens = self._estimate_tokens(prompt)
        completion_tokens = self._estimate_tokens(completion.content[0].text)
        
        self.cost_tracker["prompt_tokens"] += prompt_tokens
        self.cost_tracker["completion_tokens"] += completion_tokens
        self.cost_tracker["total_tokens"] += prompt_tokens + completion_tokens
        self.cost_tracker["requests"] += 1
        
        # Calculate cost
        model_params = self.model_params.get(model, {})
        input_cost = (prompt_tokens / 1000) * model_params.get("input_cost_per_1k", 0.01)
        output_cost = (completion_tokens / 1000) * model_params.get("output_cost_per_1k", 0.03)
        request_cost = input_cost + output_cost
        self.cost_tracker["total_cost"] += request_cost
        
        logger.info(f"Request cost: ${request_cost:.4f}, Total cost: ${self.cost_tracker['total_cost']:.4f}")
        
        return completion.content[0].text
    
    def _generate_mock(self, prompt: str, model: str, temperature: float, max_tokens: int) -> str:
        """Generate mock responses for testing."""
        # Simple mock implementation that echoes part of the prompt
        logger.warning("Using mock LLM implementation")
        
        # Wait to simulate API call
        time.sleep(1)
        
        # Create a simple response based on the prompt
        first_line = prompt.strip().split("\n")[0]
        return f"Mock response to: {first_line[:50]}...\n\nThis is a simulated response as no LLM API is configured."
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics for the LLM service."""
        return {
            "api_type": self.api_type,
            "model": self.model,
            "cache_entries": len(self.cache),
            "cache_ttl": self.cache_ttl,
            "total_tokens": self.cost_tracker["total_tokens"],
            "prompt_tokens": self.cost_tracker["prompt_tokens"],
            "completion_tokens": self.cost_tracker["completion_tokens"],
            "total_cost": self.cost_tracker["total_cost"],
            "requests": self.cost_tracker["requests"]
        }