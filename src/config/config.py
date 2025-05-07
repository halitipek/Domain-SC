"""
Configuration settings for Domain-SC system.
"""

import os
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
VECTOR_DB_PATH = DATA_DIR / "vectordb"
LOGS_DIR = BASE_DIR / "logs"

# RAG settings
RAG_SETTINGS = {
    "vector_db_path": str(VECTOR_DB_PATH),
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "similarity_top_k": 5
}

# System agent settings
SYSTEM_AGENTS = {
    "OA": {"name": "Orchestrator Agent", "max_tokens": 4000},
    "DDA": {"name": "Document Discovery Agent", "max_tokens": 4000},
    "WA": {"name": "Worker Agent", "max_tokens": 4000},
    "TAA": {"name": "Technology Analysis Agent", "max_tokens": 4000},
    "RAA": {"name": "Requirements Analysis Agent", "max_tokens": 4000},
    "OAA": {"name": "Optimization Analysis Agent", "max_tokens": 4000},
    "KAA": {"name": "Rule Analysis Agent", "max_tokens": 4000},
    "SAA": {"name": "System Architect Agent", "max_tokens": 8000},
    "MTA": {"name": "Module Design Agent", "max_tokens": 4000},
    "AEA": {"name": "API Integration Agent", "max_tokens": 4000},
    "BAA": {"name": "Dependency Analysis Agent", "max_tokens": 4000},
    "CAA": {"name": "Consistency Analysis Agent", "max_tokens": 4000}
}

# LLM settings
LLM_CONFIG = {
    "default_model": "gpt-4.1-2025-04-14",
    "fallback_model": "gpt-3.5-turbo",
    "lightweight_model": "gpt-3.5-turbo",
    "model": "gpt-4.1-2025-04-14",  # For backward compatibility
    "api_type": "openai",
    "temperature": 0.2,
    "top_p": 0.95,
    "request_timeout": 120,
    "max_retries": 3,
    "max_tokens": 4000,
    "cache_ttl": 3600  # 1 hour
}

# API configuration
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "debug": False
}

# Agent settings
AGENT_SETTINGS = {
    "default_timeout": 120,  # seconds
    "max_retries": 3,
    "debug_mode": False
}

# Create necessary directories
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(VECTOR_DB_PATH, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
