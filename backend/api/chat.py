from fastapi import APIRouter
from pydantic import BaseModel

from rag.pipeline import run_rag_pipeline

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):

    response = run_rag_pipeline(req.query)

    return ChatResponse(answer=response)