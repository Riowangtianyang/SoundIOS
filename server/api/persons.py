from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from services.supabase_db import (
    create_person as db_create_person,
    get_persons as db_get_persons,
    get_person as db_get_person,
    update_person as db_update_person,
    delete_person as db_delete_person,
    create_memory as db_create_memory,
    get_memories as db_get_memories,
    update_memory_confirmed as db_update_memory_confirmed,
)

router = APIRouter()


class PersonCreate(BaseModel):
    name: str
    relationship_type: Optional[str] = None
    notes: Optional[str] = None
    personality_tags: Optional[List[str]] = None


class PersonUpdate(BaseModel):
    name: Optional[str] = None
    relationship_type: Optional[str] = None
    notes: Optional[str] = None
    personality_tags: Optional[List[str]] = None


class MemoryCreate(BaseModel):
    person_id: Optional[int] = None
    content: str
    category: Optional[str] = None
    confirmed: Optional[int] = 0


@router.get("/persons")
async def list_persons():
    """获取人物列表"""
    persons = db_get_persons()
    return {
        "persons": [
            {
                "id": p["id"],
                "name": p["name"],
                "relationship_type": p.get("relationship_type"),
                "notes": p.get("notes"),
                "personality_tags": p.get("personality_tags") or []
            }
            for p in persons
        ]
    }


@router.post("/persons")
async def create_person(person: PersonCreate):
    """创建人物"""
    # 检查是否已存在
    existing = db_get_persons()
    for p in existing:
        if p["name"] == person.name:
            raise HTTPException(status_code=400, detail="该人物已存在")

    new_person = db_create_person(
        name=person.name,
        relationship_type=person.relationship_type,
        notes=person.notes,
        personality_tags=person.personality_tags
    )

    return {
        "id": new_person["id"],
        "name": new_person["name"],
        "relationship_type": new_person.get("relationship_type"),
        "notes": new_person.get("notes"),
        "personality_tags": new_person.get("personality_tags") or []
    }


@router.get("/persons/{person_id}")
async def get_person(person_id: int):
    """获取人物详情"""
    person = db_get_person(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="人物不存在")

    # 获取该人物的内存
    memories = db_get_memories(person_id=person_id)

    return {
        "id": person["id"],
        "name": person["name"],
        "relationship_type": person.get("relationship_type"),
        "notes": person.get("notes"),
        "personality_tags": person.get("personality_tags") or [],
        "memories": [
            {
                "id": m["id"],
                "content": m["content"],
                "category": m.get("category"),
                "confirmed": m.get("confirmed")
            }
            for m in memories
        ]
    }


@router.put("/persons/{person_id}")
async def update_person(person_id: int, person_update: PersonUpdate):
    """更新人物信息"""
    existing = db_get_person(person_id)
    if not existing:
        raise HTTPException(status_code=404, detail="人物不存在")

    update_data = {}
    if person_update.name is not None:
        update_data["name"] = person_update.name
    if person_update.relationship_type is not None:
        update_data["relationship_type"] = person_update.relationship_type
    if person_update.notes is not None:
        update_data["notes"] = person_update.notes
    if person_update.personality_tags is not None:
        update_data["personality_tags"] = person_update.personality_tags

    updated = db_update_person(person_id, update_data)

    return {
        "id": updated["id"],
        "name": updated["name"],
        "relationship_type": updated.get("relationship_type"),
        "notes": updated.get("notes"),
        "personality_tags": updated.get("personality_tags") or []
    }


@router.delete("/persons/{person_id}")
async def delete_person(person_id: int):
    """删除人物"""
    existing = db_get_person(person_id)
    if not existing:
        raise HTTPException(status_code=404, detail="人物不存在")

    db_delete_person(person_id)

    return {"message": "人物已删除"}


@router.get("/memories")
async def list_memories(
    person_id: Optional[int] = None,
    category: Optional[str] = None,
    confirmed: Optional[int] = None,
):
    """获取记忆列表"""
    memories = db_get_memories(person_id=person_id, confirmed=confirmed)

    if category:
        memories = [m for m in memories if m.get("category") == category]

    return [
        {
            "id": m["id"],
            "person_id": m.get("person_id"),
            "content": m["content"],
            "category": m.get("category"),
            "confirmed": m.get("confirmed")
        }
        for m in memories
    ]


@router.post("/memories")
async def create_memory(memory: MemoryCreate):
    """创建记忆"""
    new_memory = db_create_memory(
        content=memory.content,
        person_id=memory.person_id,
        category=memory.category,
        confirmed=memory.confirmed or 0
    )

    return {
        "id": new_memory["id"],
        "person_id": new_memory.get("person_id"),
        "content": new_memory["content"],
        "category": new_memory.get("category"),
        "confirmed": new_memory.get("confirmed")
    }


@router.put("/memories/{memory_id}/confirm")
async def confirm_memory(memory_id: int):
    """确认记忆"""
    memories = db_get_memories()
    memory = next((m for m in memories if m["id"] == memory_id), None)

    if not memory:
        raise HTTPException(status_code=404, detail="记忆不存在")

    updated = db_update_memory_confirmed(memory_id, 1)

    return {
        "id": updated["id"],
        "person_id": updated.get("person_id"),
        "content": updated["content"],
        "category": updated.get("category"),
        "confirmed": updated.get("confirmed")
    }