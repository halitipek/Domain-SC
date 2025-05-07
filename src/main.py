import os
import uvicorn
import logging
from fastapi import FastAPI, HTTPException
from pathlib import Path

from src.config.config import API_CONFIG
from src.utils.logger import setup_logger
from src.api.router import router

# Set up logging
logger = setup_logger(__name__, "main.log")

# Create FastAPI app
app = FastAPI(
    title="Domain-SC - Multi-Agent System Architecture Design",
    description="A multi-agent system for creating system architecture documents",
    version="0.1.0"
)

# Add router
app.include_router(router)

@app.get("/", tags=["Root"])
async def read_root():
    return {
        "message": "Domain-SC API is running",
        "endpoints": [
            "/api/v1/status",
            "/api/v1/documents/index",
            "/api/v1/documents/stats",
            "/api/v1/rag/query",
            "/api/v1/rag/clear",
            "/api/v1/context/{agent_type}"
        ]
    }

@app.on_event("startup")
async def startup_event():
    logger.info("Starting Domain-SC API")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Domain-SC API")

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=API_CONFIG["host"],
        port=API_CONFIG["port"],
        reload=API_CONFIG["debug"]
    )
