from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from models import get_db
from models.database import Person, Memory

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
async def list_persons(db: Session = Depends(get_db)):
    """获取人物列表"""
    persons = db.query(Person).all()
    return {
        "persons": [
            {
                "id": p.id,
                "name": p.name,
                "relationship_type": p.relationship_type,
                "notes": p.notes,
                "personality_tags": p.personality_tags
            }
            for p in persons
        ]
    }


@router.post("/persons")
async def create_person(person: PersonCreate, db: Session = Depends(get_db)):
    """创建人物"""
    existing = db.query(Person).filter(Person.name == person.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="该人物已存在")

    new_person = Person(
        name=person.name,
        relationship_type=person.relationship_type,
        notes=person.notes,
        personality_tags=person.personality_tags
    )
    db.add(new_person)
    db.commit()
    db.refresh(new_person)

    return {
        "id": new_person.id,
        "name": new_person.name,
        "relationship_type": new_person.relationship_type,
        "notes": new_person.notes,
        "personality_tags": new_person.personality_tags
    }


@router.get("/persons/{person_id}")
async def get_person(person_id: int, db: Session = Depends(get_db)):
    """获取人物详情"""
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="人物不存在")

    return {
        "id": person.id,
        "name": person.name,
        "relationship_type": person.relationship_type,
        "notes": person.notes,
        "personality_tags": person.personality_tags,
        "memories": [
            {
                "id": m.id,
                "content": m.content,
                "category": m.category,
                "confirmed": m.confirmed
            }
            for m in person.memories
        ]
    }


@router.put("/persons/{person_id}")
async def update_person(person_id: int, person_update: PersonUpdate, db: Session = Depends(get_db)):
    """更新人物信息"""
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="人物不存在")

    if person_update.name is not None:
        person.name = person_update.name
    if person_update.relationship_type is not None:
        person.relationship_type = person_update.relationship_type
    if person_update.notes is not None:
        person.notes = person_update.notes
    if person_update.personality_tags is not None:
        person.personality_tags = person_update.personality_tags

    db.commit()
    db.refresh(person)

    return {
        "id": person.id,
        "name": person.name,
        "relationship_type": person.relationship_type,
        "notes": person.notes,
        "personality_tags": person.personality_tags
    }


@router.delete("/persons/{person_id}")
async def delete_person(person_id: int, db: Session = Depends(get_db)):
    """删除人物"""
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="人物不存在")

    db.delete(person)
    db.commit()

    return {"message": "人物已删除"}


@router.get("/memories")
async def list_memories(
    person_id: Optional[int] = None,
    category: Optional[str] = None,
    confirmed: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """获取记忆列表"""
    query = db.query(Memory)

    if person_id is not None:
        query = query.filter(Memory.person_id == person_id)
    if category:
        query = query.filter(Memory.category == category)
    if confirmed is not None:
        query = query.filter(Memory.confirmed == confirmed)

    memories = query.all()

    return [
        {
            "id": m.id,
            "person_id": m.person_id,
            "content": m.content,
            "category": m.category,
            "confirmed": m.confirmed
        }
        for m in memories
    ]


@router.post("/memories")
async def create_memory(memory: MemoryCreate, db: Session = Depends(get_db)):
    """创建记忆"""
    new_memory = Memory(
        person_id=memory.person_id,
        content=memory.content,
        category=memory.category,
        confirmed=memory.confirmed or 0
    )
    db.add(new_memory)
    db.commit()
    db.refresh(new_memory)

    return {
        "id": new_memory.id,
        "person_id": new_memory.person_id,
        "content": new_memory.content,
        "category": new_memory.category,
        "confirmed": new_memory.confirmed
    }


@router.put("/memories/{memory_id}/confirm")
async def confirm_memory(memory_id: int, db: Session = Depends(get_db)):
    """确认记忆"""
    memory = db.query(Memory).filter(Memory.id == memory_id).first()
    if not memory:
        raise HTTPException(status_code=404, detail="记忆不存在")

    memory.confirmed = 1
    db.commit()
    db.refresh(memory)

    return {
        "id": memory.id,
        "person_id": memory.person_id,
        "content": memory.content,
        "category": memory.category,
        "confirmed": memory.confirmed
    }