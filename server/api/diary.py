from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models import get_db
from models.database import DiaryEntry

router = APIRouter()


class DiaryEntryCreate(BaseModel):
    date: Optional[datetime] = None
    summary: str
    details: Optional[str] = None
    mood_score: Optional[int] = None


class DiaryEntryUpdate(BaseModel):
    summary: Optional[str] = None
    details: Optional[str] = None
    mood_score: Optional[int] = None


@router.get("/diaries")
async def list_diaries(db: Session = Depends(get_db)):
    """获取日记列表"""
    diaries = db.query(DiaryEntry).order_by(DiaryEntry.date.desc()).all()
    return {
        "diaries": [
            {
                "id": d.id,
                "date": d.date,
                "summary": d.summary,
                "details": d.details,
                "mood_score": d.mood_score
            }
            for d in diaries
        ]
    }


@router.post("/diaries")
async def create_diary(entry: DiaryEntryCreate, db: Session = Depends(get_db)):
    """创建日记"""
    diary = DiaryEntry(
        date=entry.date or datetime.utcnow(),
        summary=entry.summary,
        details=entry.details,
        mood_score=entry.mood_score
    )
    db.add(diary)
    db.commit()
    db.refresh(diary)

    return {
        "id": diary.id,
        "date": diary.date,
        "summary": diary.summary,
        "details": diary.details,
        "mood_score": diary.mood_score
    }


@router.get("/diaries/{diary_id}")
async def get_diary(diary_id: int, db: Session = Depends(get_db)):
    """获取日记详情"""
    diary = db.query(DiaryEntry).filter(DiaryEntry.id == diary_id).first()
    if not diary:
        raise HTTPException(status_code=404, detail="日记不存在")

    return {
        "id": diary.id,
        "date": diary.date,
        "summary": diary.summary,
        "details": diary.details,
        "mood_score": diary.mood_score
    }


@router.put("/diaries/{diary_id}")
async def update_diary(diary_id: int, entry: DiaryEntryUpdate, db: Session = Depends(get_db)):
    """更新日记"""
    diary = db.query(DiaryEntry).filter(DiaryEntry.id == diary_id).first()
    if not diary:
        raise HTTPException(status_code=404, detail="日记不存在")

    if entry.summary is not None:
        diary.summary = entry.summary
    if entry.details is not None:
        diary.details = entry.details
    if entry.mood_score is not None:
        diary.mood_score = entry.mood_score

    db.commit()
    db.refresh(diary)

    return {
        "id": diary.id,
        "date": diary.date,
        "summary": diary.summary,
        "details": diary.details,
        "mood_score": diary.mood_score
    }


@router.delete("/diaries/{diary_id}")
async def delete_diary(diary_id: int, db: Session = Depends(get_db)):
    """删除日记"""
    diary = db.query(DiaryEntry).filter(DiaryEntry.id == diary_id).first()
    if not diary:
        raise HTTPException(status_code=404, detail="日记不存在")

    db.delete(diary)
    db.commit()

    return {"message": "日记已删除"}


@router.get("/diaries/date/{date_str}")
async def get_diary_by_date(date_str: str, db: Session = Depends(get_db)):
    """根据日期字符串获取日记"""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="日期格式错误，请使用 YYYY-MM-DD")

    diary = db.query(DiaryEntry).filter(
        DiaryEntry.date >= date,
        DiaryEntry.date < date.replace(hour=23, minute=59, second=59)
    ).first()

    if not diary:
        return {
            "date": date_str,
            "summary": "今日暂无记录",
            "details": None,
            "mood_score": None
        }

    return {
        "id": diary.id,
        "date": diary.date,
        "summary": diary.summary,
        "details": diary.details,
        "mood_score": diary.mood_score
    }