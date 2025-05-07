"""
Configuration module for the CLI.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# User config file location
CONFIG_DIR = Path.home() / ".config" / "domain-sc"
CONFIG_FILE = CONFIG_DIR / "config.json"


class CliConfig:
    """
    Configuration class for the CLI application.
    Handles loading configuration from environment variables and config files.
    """
    
    def __init__(self):
        """Initialize configuration with defaults and load from file and environment."""
        # Default configuration
        self.config: Dict[str, Any] = {
            "llm": {
                "default_model": "gpt-4",
                "default_temperature": 0.7,
                "default_max_tokens": 1000,
            },
            "rag": {
                "default_collection": "default",
                "default_top_k": 5,
                "vectordb_path": str(ROOT_DIR / "data" / "vectordb"),
            },
            "workflow": {
                "output_path": str(ROOT_DIR / "data" / "output"),
            },
            "logging": {
                "level": "INFO",
                "log_dir": str(ROOT_DIR / "logs"),
            }
        }
        
        # Load configuration from file
        self._load_from_file()
        
        # Override with environment variables
        self._load_from_env()
    
    def _load_from_file(self) -> None:
        """Load configuration from the config file if it exists."""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r') as f:
                    file_config = json.load(f)
                    self._merge_config(file_config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Failed to load config file: {e}")
    
    def _load_from_env(self) -> None:
        """Load configuration from environment variables."""
        # LLM settings
        if os.environ.get("DOMAIN_SC_LLM_MODEL"):
            self.config["llm"]["default_model"] = os.environ.get("DOMAIN_SC_LLM_MODEL")
        
        if os.environ.get("DOMAIN_SC_LLM_TEMPERATURE"):
            try:
                temp = float(os.environ.get("DOMAIN_SC_LLM_TEMPERATURE", "0.7"))
                self.config["llm"]["default_temperature"] = temp
            except ValueError:
                pass
        
        if os.environ.get("DOMAIN_SC_LLM_MAX_TOKENS"):
            try:
                tokens = int(os.environ.get("DOMAIN_SC_LLM_MAX_TOKENS", "1000"))
                self.config["llm"]["default_max_tokens"] = tokens
            except ValueError:
                pass
        
        # RAG settings
        if os.environ.get("DOMAIN_SC_RAG_COLLECTION"):
            self.config["rag"]["default_collection"] = os.environ.get("DOMAIN_SC_RAG_COLLECTION")
        
        if os.environ.get("DOMAIN_SC_RAG_TOP_K"):
            try:
                top_k = int(os.environ.get("DOMAIN_SC_RAG_TOP_K", "5"))
                self.config["rag"]["default_top_k"] = top_k
            except ValueError:
                pass
        
        if os.environ.get("DOMAIN_SC_VECTORDB_PATH"):
            self.config["rag"]["vectordb_path"] = os.environ.get("DOMAIN_SC_VECTORDB_PATH")
        
        # Workflow settings
        if os.environ.get("DOMAIN_SC_OUTPUT_PATH"):
            self.config["workflow"]["output_path"] = os.environ.get("DOMAIN_SC_OUTPUT_PATH")
        
        # Logging settings
        if os.environ.get("DOMAIN_SC_LOG_LEVEL"):
            self.config["logging"]["level"] = os.environ.get("DOMAIN_SC_LOG_LEVEL")
        
        if os.environ.get("DOMAIN_SC_LOG_DIR"):
            self.config["logging"]["log_dir"] = os.environ.get("DOMAIN_SC_LOG_DIR")
    
    def _merge_config(self, config_dict: Dict[str, Any]) -> None:
        """
        Recursively merge the provided config dictionary into the current config.
        
        Args:
            config_dict: Dictionary containing configuration to merge
        """
        for key, value in config_dict.items():
            if key in self.config and isinstance(self.config[key], dict) and isinstance(value, dict):
                self._merge_config_dict(self.config[key], value)
            else:
                self.config[key] = value
    
    def _merge_config_dict(self, target: Dict[str, Any], source: Dict[str, Any]) -> None:
        """
        Helper method to recursively merge nested dictionaries.
        
        Args:
            target: Target dictionary to merge into
            source: Source dictionary to merge from
        """
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._merge_config_dict(target[key], value)
            else:
                target[key] = value
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            default: Default value if not found
            
        Returns:
            The configuration value or default
        """
        if section in self.config and key in self.config[section]:
            return self.config[section][key]
        return default
    
    def save(self) -> None:
        """Save the current configuration to the config file."""
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=2)
        except IOError as e:
            print(f"Warning: Failed to save config file: {e}")