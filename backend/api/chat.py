from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from rag.pipeline import run_rag_pipeline

router = APIRouter()


class ChatRequest(BaseModel):
    query: str
    mode: str = "student"


class ChatResponse(BaseModel):
    answer: str
    confidence: str
    reason: str
    sources: List[str]


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):

    result = run_rag_pipeline(req.query, req.mode)

    return ChatResponse(
        answer=result["answer"],
        confidence=result["confidence"],
        reason=result["reason"],
        sources=result["sources"]
    )