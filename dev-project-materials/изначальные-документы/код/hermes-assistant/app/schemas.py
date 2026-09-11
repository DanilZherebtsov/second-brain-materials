from typing import Literal, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    session_id: Optional[str] = None
    channel: Literal["chat", "email"] = "chat"


class Citation(BaseModel):
    doc_id: str
    title: str
    clause: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation] = []
    confidence: float = Field(..., ge=0.0, le=1.0)
    latency_ms: int = 0


class RegulationOut(BaseModel):
    doc_id: str
    title: str
    text: str
