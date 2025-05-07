"""
API Router for the Domain-SC system.
This module provides the API endpoints for interacting with the system.
"""

from fastapi import APIRouter, HTTPException, Depends, Body, Query, Path
from typing import List, Dict, Any, Optional

from src.models.base_models import AgentMessage, AgentTask, Document
from src.services.rag_service import RagService
from src.services.workflow_service import WorkflowService
from src.services.llm_service import LLMService
from src.prompts.prompt_manager import PromptManager

# Create API router
router = APIRouter(prefix="/api/v1", tags=["Domain-SC API"])

# Create service instances
rag_service = RagService()
workflow_service = WorkflowService()
llm_service = LLMService()
prompt_manager = PromptManager()

# RAG endpoints
@router.get("/status")
async def get_status():
    """Get system status."""
    return {
        "status": "operational",
        "rag_service": rag_service.get_stats(),
        "workflow_service": workflow_service.get_workflow_status()
    }

@router.post("/documents/index")
async def index_documents(file_paths: List[str] = Body(...), 
                       collection_name: Optional[str] = Body(None)):
    """Index documents for RAG."""
    result = rag_service.index_documents(file_paths, collection_name)
    return result

@router.get("/documents/stats")
async def get_document_stats():
    """Get document and vector store statistics."""
    return rag_service.get_stats()

@router.post("/rag/query")
async def query_rag(query: str = Body(...), 
                 agent_type: Optional[str] = Body(None),
                 top_k: Optional[int] = Body(None)):
    """Query the RAG service."""
    result = rag_service.query(query, agent_type, top_k)
    return result

@router.delete("/rag/clear")
async def clear_rag_index():
    """Clear the RAG vector store index."""
    rag_service.clear_index()
    return {"status": "success", "message": "RAG index cleared successfully"}

@router.get("/context/{agent_type}")
async def get_agent_context(agent_type: str, query: str = Query(...)):
    """Get context for a specific agent type."""
    context = rag_service.get_context_for_agent(query, agent_type)
    return context

# Workflow endpoints
@router.post("/workflows")
async def create_workflow(workflow_name: str = Body(...), 
                        input_files: List[str] = Body(...)):
    """Create a new workflow."""
    result = await workflow_service.initialize_workflow(workflow_name, input_files)
    return result

@router.get("/workflows")
async def get_workflows():
    """Get all workflows."""
    return workflow_service.get_workflow_status()

@router.get("/workflows/{workflow_id}")
async def get_workflow(workflow_id: str):
    """Get a specific workflow."""
    result = workflow_service.get_workflow_status(workflow_id)
    if "status" in result and result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    return result

@router.post("/workflows/{workflow_id}/advance")
async def advance_workflow(workflow_id: str, next_phase: str = Body(...)):
    """Advance a workflow to the next phase."""
    result = await workflow_service.advance_workflow(workflow_id, next_phase)
    if "status" in result and result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    return result

@router.post("/workflows/{workflow_id}/tasks")
async def send_task(workflow_id: str, 
                  agent_id: str = Body(...),
                  task_description: str = Body(...),
                  task_type: str = Body(...),
                  input_data: Dict[str, Any] = Body(...)):
    """Send a task to an agent."""
    result = await workflow_service.send_direct_task(
        workflow_id=workflow_id,
        agent_id=agent_id,
        task_description=task_description,
        task_type=task_type,
        input_data=input_data
    )
    if "status" in result and result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    return result

@router.post("/workflows/{workflow_id}/results")
async def collect_results(workflow_id: str, task_ids: List[str] = Body(...)):
    """Collect results from tasks."""
    result = await workflow_service.collect_task_results(workflow_id, task_ids)
    if "status" in result and result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    return result

@router.post("/workflows/{workflow_id}/finalize")
async def finalize_workflow(workflow_id: str):
    """Finalize a workflow."""
    result = await workflow_service.finalize_workflow(workflow_id)
    if "status" in result and result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    return result

# LLM endpoints
@router.post("/llm/generate")
async def generate_text(prompt: str = Body(...),
                     model: Optional[str] = Body(None),
                     temperature: Optional[float] = Body(None),
                     max_tokens: Optional[int] = Body(None)):
    """Generate text using the LLM service."""
    response = llm_service.generate_text(
        prompt=prompt,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return {"response": response}

@router.post("/llm/agent-prompt")
async def generate_with_agent_prompt(agent_id: str = Body(...),
                                 prompt_type: str = Body(...),
                                 variables: Dict[str, Any] = Body({}),
                                 model: Optional[str] = Body(None),
                                 temperature: Optional[float] = Body(None),
                                 max_tokens: Optional[int] = Body(None)):
    """Generate text using an agent's prompt template."""
    response = llm_service.generate_with_agent_prompt(
        agent_id=agent_id,
        prompt_type=prompt_type,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        **variables
    )
    return {"response": response}

# Prompt endpoints
@router.get("/prompts/templates")
async def get_prompt_templates():
    """Get all available prompt templates."""
    templates = {}
    for agent_id in prompt_manager.templates:
        templates[agent_id] = list(prompt_manager.templates[agent_id].keys())
    return {"templates": templates}

@router.get("/prompts/templates/{agent_id}")
async def get_agent_templates(agent_id: str):
    """Get prompt templates for a specific agent."""
    template = prompt_manager.get_template(agent_id)
    if not template:
        raise HTTPException(status_code=404, detail=f"No templates found for agent {agent_id}")
    return {"agent_id": agent_id, "templates": template}

@router.post("/prompts/templates/{agent_id}")
async def save_agent_template(agent_id: str, template_data: Dict[str, Any] = Body(...)):
    """Save a prompt template for an agent."""
    result = prompt_manager.save_template(agent_id, template_data)
    if not result:
        raise HTTPException(status_code=500, detail=f"Failed to save template for agent {agent_id}")
    return {"status": "success", "agent_id": agent_id}