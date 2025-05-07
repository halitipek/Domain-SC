"""
LLM Service for the Domain-SC system.
This service manages interactions with LLM providers and ensures proper prompt formatting.
"""

import os
import json
import logging
import time
from typing import Dict, Any, Optional, List, Union
from datetime import datetime

from src.config.config import LLM_CONFIG
from src.utils.logger import setup_logger
from src.prompts.prompt_manager import PromptManager

from dotenv import load_dotenv

logger = setup_logger(__name__, "llm_service.log")

class LLMService:
    """Service for managing LLM interactions."""
    
    def __init__(self):
        """Initialize the LLM service."""
        self.config = LLM_CONFIG
        self.prompt_manager = PromptManager()
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
        
        # Request cache to avoid duplicate requests
        self.cache = {}
        self.cache_ttl = 3600  # 1 hour
        
        logger.info(f"LLM Service initialized with model: {self.model}")
    
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
    
    def _get_cache_key(self, prompt: str, model: str, temperature: float) -> str:
        """Generate a cache key for a request."""
        # Simple cache key - in production, you might want to use a hash
        return f"{model}_{temperature}_{prompt[:100]}"
    
    def _check_cache(self, prompt: str, model: str, temperature: float) -> Optional[str]:
        """Check if a response is cached."""
        cache_key = self._get_cache_key(prompt, model, temperature)
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
        cache_key = self._get_cache_key(prompt, model, temperature)
        self.cache[cache_key] = (datetime.now().timestamp(), response)
        
        # Clean up old cache entries
        self._clean_cache()
    
    def _clean_cache(self):
        """Clean up old cache entries."""
        now = datetime.now().timestamp()
        expired_keys = [k for k, v in self.cache.items() if (now - v[0]) > self.cache_ttl]
        for key in expired_keys:
            del self.cache[key]
    
    def generate_text(self, 
                     prompt: str, 
                     model: Optional[str] = None, 
                     temperature: Optional[float] = None, 
                     max_tokens: Optional[int] = None,
                     use_cache: bool = True) -> str:
        """Generate text from a prompt using the configured LLM.
        
        Args:
            prompt: The prompt to send to the LLM
            model: Optional model override
            temperature: Optional temperature override
            max_tokens: Optional max_tokens override
            use_cache: Whether to use the cache
            
        Returns:
            Generated text from the LLM, or error message if generation fails
        """
        if not prompt or not isinstance(prompt, str):
            logger.error(f"Invalid prompt: {type(prompt)}")
            return "Error: Invalid prompt"
            
        # Use defaults if not provided
        model = model or self.model
        temperature = temperature if temperature is not None else self.temperature
        # Validate temperature is in valid range
        if temperature < 0 or temperature > 1:
            logger.warning(f"Temperature {temperature} outside valid range [0-1], clamping")
            temperature = max(0, min(1, temperature))
        
        max_tokens = max_tokens or 4000
        if max_tokens <= 0:
            logger.warning(f"Invalid max_tokens {max_tokens}, using default")
            max_tokens = 4000
        
        # Check cache if enabled
        if use_cache:
            cached_response = self._check_cache(prompt, model, temperature)
            if cached_response:
                return cached_response
        
        # Count tokens (approximate)
        try:
            estimated_prompt_tokens = len(prompt.split()) * 1.3
            logger.info(f"Sending prompt to {model} (est. {int(estimated_prompt_tokens)} tokens)")
        except Exception as token_err:
            logger.warning(f"Error estimating tokens: {str(token_err)}")
        
        # Generate response based on API type
        response = ""
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
                
                # Cache the successful response if caching is enabled
                if use_cache and response:
                    self._update_cache(prompt, model, temperature, response)
                
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
        """Generate text using OpenAI API."""
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
        
        return completion.choices[0].message.content
    
    def _generate_anthropic(self, prompt: str, model: str, temperature: float, max_tokens: int) -> str:
        """Generate text using Anthropic API."""
        if not self.client:
            return "Anthropic client not initialized"
        
        completion = self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        
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
    
    def generate_with_agent_prompt(self, 
                                  agent_id: str, 
                                  prompt_type: str,
                                  model: Optional[str] = None,
                                  temperature: Optional[float] = None,
                                  max_tokens: Optional[int] = None,
                                  use_cache: bool = True,
                                  **kwargs) -> str:
        """Generate text using a template from the prompt manager.
        
        Args:
            agent_id: The ID of the agent (e.g., "SAA", "RAA")
            prompt_type: The type of prompt (e.g., "task_execution", "query_processing")
            model: Optional model override
            temperature: Optional temperature override
            max_tokens: Optional max_tokens override
            use_cache: Whether to use the cache
            **kwargs: Variables to format the prompt template with
            
        Returns:
            Generated text from the LLM
        """
        # Get the formatted prompt from the prompt manager
        formatted_prompt = self.prompt_manager.get_prompt(agent_id, prompt_type, **kwargs)
        
        # Generate text with the formatted prompt
        return self.generate_text(
            prompt=formatted_prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            use_cache=use_cache
        )
    
    def generate_rag_enhanced_response(self,
                                      agent_id: str,
                                      prompt_type: str,
                                      query: str,
                                      rag_context: List[Dict[str, Any]],
                                      model: Optional[str] = None,
                                      temperature: Optional[float] = None,
                                      max_tokens: Optional[int] = None,
                                      use_cache: bool = True,
                                      **kwargs) -> str:
        """Generate a response enhanced with RAG context.
        
        Args:
            agent_id: The ID of the agent (e.g., "SAA", "RAA")
            prompt_type: The type of prompt (e.g., "task_execution", "query_processing")
            query: The query or task to respond to
            rag_context: List of context documents from RAG
            model: Optional model override
            temperature: Optional temperature override
            max_tokens: Optional max_tokens override
            use_cache: Whether to use the cache
            **kwargs: Additional variables for prompt formatting
            
        Returns:
            Generated text from the LLM
        """
        # Get the formatted prompt from the prompt manager
        base_prompt = self.prompt_manager.get_prompt(agent_id, prompt_type, query=query, **kwargs)
        
        # Format the RAG context as a string
        context_str = "Context information:\n\n"
        for i, doc in enumerate(rag_context, 1):
            content = doc.get("content", "")
            source = doc.get("metadata", {}).get("source", "unknown")
            context_str += f"[Document {i}] From: {source}\n{content}\n\n"
        
        # Combine the base prompt with the RAG context
        enhanced_prompt = f"{base_prompt}\n\n{context_str}\n\nAnswer based on the above context:"
        
        # Generate text with the enhanced prompt
        return self.generate_text(
            prompt=enhanced_prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            use_cache=use_cache
        )
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics for the LLM service."""
        return {
            "api_type": self.api_type,
            "model": self.model,
            "cache_entries": len(self.cache),
            "cache_ttl": self.cache_ttl
        }