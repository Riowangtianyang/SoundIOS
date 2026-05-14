from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
from services.supabase_db import get_person, get_persons, get_memories
from services.llm import get_llm_service
from services.analyzer import analyze_conversation
from services.tts import text_to_speech

router = APIRouter()


class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
    context: Optional[Dict] = None
    return_audio: bool = False  # 是否返回语音


class ProcessTranscriptRequest(BaseModel):
    recording_id: int
    transcript_text: Optional[str] = None


@router.post("/chat")
async def chat(request: ChatRequest):
    """与 AI 对话"""
    messages = [{"role": m.role, "content": m.content} for m in request.messages]
    llm_service = get_llm_service()
    response = await llm_service.chat(messages)

    # 如果请求语音回复
    if request.return_audio:
        audio_stream = text_to_speech(response)
        return StreamingResponse(
            audio_stream,
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline"}
        )

    return {"response": response}


@router.post("/chat/process")
async def process_transcript(request: ProcessTranscriptRequest):
    """处理录音转写的文本，提取关键信息"""
    if not request.transcript_text:
        raise HTTPException(status_code=400, detail="转写文本不能为空")

    analysis = await analyze_conversation(request.transcript_text)

    return analysis


@router.get("/chat/context")
async def get_chat_context(person_id: Optional[int] = None):
    """获取聊天上下文信息"""
    context = {}

    if person_id:
        person = get_person(person_id)
        if person:
            context["person"] = {
                "id": person.get("id"),
                "name": person.get("name"),
                "relationship": person.get("relationship_type"),
                "notes": person.get("notes"),
                "personality_tags": person.get("personality_tags") or []
            }
            memories = get_memories(person_id=person_id, confirmed=True)
            context["memories"] = [
                {
                    "id": m.get("id"),
                    "content": m.get("content"),
                    "category": m.get("category"),
                    "confirmed": m.get("confirmed")
                }
                for m in memories
            ]
    else:
        memories = get_memories(confirmed=True)
        context["memories"] = [
            {
                "id": m.get("id"),
                "content": m.get("content"),
                "category": m.get("category"),
                "confirmed": m.get("confirmed")
            }
            for m in memories
        ]

        persons = get_persons()
        context["persons"] = [
            {
                "id": p.get("id"),
                "name": p.get("name"),
                "relationship": p.get("relationship_type"),
                "personality_tags": p.get("personality_tags") or []
            }
            for p in persons
        ]

    return context


@router.get("/chat/voices")
async def list_voices():
    """获取可用语音列表"""
    from services.tts import AVAILABLE_VOICES
    return {"voices": AVAILABLE_VOICES}