from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Dict
from models import get_db
from models.database import Person, Memory
from services.llm import get_llm_service
from services.analyzer import analyze_conversation

router = APIRouter()


class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
    context: Optional[Dict] = None


class ProcessTranscriptRequest(BaseModel):
    recording_id: int
    transcript_text: Optional[str] = None


@router.post("/chat")
async def chat(request: ChatRequest):
    """与 AI 对话"""
    messages = [{"role": m.role, "content": m.content} for m in request.messages]
    llm_service = get_llm_service()
    response = await llm_service.chat(messages)

    return {"response": response}


@router.post("/chat/process")
async def process_transcript(request: ProcessTranscriptRequest, db: Session = Depends(get_db)):
    """处理录音转写的文本，提取关键信息"""
    if not request.transcript_text:
        raise HTTPException(status_code=400, detail="转写文本不能为空")

    analysis = await analyze_conversation(request.transcript_text)

    return analysis


@router.get("/chat/context")
async def get_chat_context(
    person_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """获取聊天上下文信息"""
    context = {}

    if person_id:
        person = db.query(Person).filter(Person.id == person_id).first()
        if person:
            context["person"] = {
                "id": person.id,
                "name": person.name,
                "relationship": person.relationship_type,
                "notes": person.notes,
                "personality_tags": person.personality_tags
            }
            context["memories"] = [
                {
                    "id": m.id,
                    "content": m.content,
                    "category": m.category,
                    "confirmed": m.confirmed
                }
                for m in person.memories if m.confirmed == 1
            ]
    else:
        memories = db.query(Memory).filter(Memory.confirmed == 1).all()
        context["memories"] = [
            {
                "id": m.id,
                "content": m.content,
                "category": m.category,
                "confirmed": m.confirmed
            }
            for m in memories
        ]

        persons = db.query(Person).all()
        context["persons"] = [
            {
                "id": p.id,
                "name": p.name,
                "relationship": p.relationship_type,
                "personality_tags": p.personality_tags
            }
            for p in persons
        ]

    return context