from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field

class Document(BaseModel):
    """Represents a document in the system."""
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AgentMessage(BaseModel):
    """Message passed between agents."""
    sender: str
    recipient: str
    content: Union[str, Dict[str, Any]]
    message_type: str = "text"
    timestamp: Optional[str] = None
    references: List[str] = Field(default_factory=list)

class AgentTask(BaseModel):
    """Task for an agent to perform."""
    task_id: str
    agent_id: str
    description: str
    task_type: str
    input_data: Dict[str, Any] = Field(default_factory=dict)
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    priority: int = 1  # 1 (highest) to 5 (lowest)
    dependencies: List[str] = Field(default_factory=list)  # List of task_ids

class AgentQuery(BaseModel):
    """Query from one agent to another."""
    query_id: str
    sender: str
    recipient: str
    content: str
    context: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None

class AgentResponse(BaseModel):
    """Response to a query from one agent to another."""
    query_id: str
    sender: str
    recipient: str
    content: str
    sources: List[Dict[str, Any]] = Field(default_factory=list)
    timestamp: Optional[str] = None

class RagQueryResult(BaseModel):
    """Results from a RAG query."""
    query: str
    retrieved_documents: List[Document] = Field(default_factory=list)
    answer: Optional[str] = None
    source_documents: List[Dict[str, Any]] = Field(default_factory=list)
