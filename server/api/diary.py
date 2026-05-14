from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.supabase_db import (
    create_diary,
    get_diaries,
    get_diary_by_date,
    update_diary as supabase_update_diary
)

router = APIRouter()


class DiaryEntryCreate(BaseModel):
    date: Optional[str] = None
    summary: str
    details: Optional[str] = None
    mood_score: Optional[int] = None


class DiaryEntryUpdate(BaseModel):
    summary: Optional[str] = None
    details: Optional[str] = None
    mood_score: Optional[int] = None


@router.get("/diaries")
async def list_diaries(limit: int = 30):
    """获取日记列表"""
    diaries = get_diaries(limit=limit)
    return {
        "diaries": [
            {
                "id": d.get("id"),
                "date": d.get("date"),
                "summary": d.get("summary"),
                "details": d.get("details"),
                "mood_score": d.get("mood_score")
            }
            for d in diaries
        ]
    }


@router.post("/diaries")
async def create_diary_entry(entry: DiaryEntryCreate):
    """创建日记"""
    diary = create_diary(
        date=entry.date,
        summary=entry.summary,
        details=entry.details,
        mood_score=entry.mood_score
    )

    return {
        "id": diary.get("id"),
        "date": diary.get("date"),
        "summary": diary.get("summary"),
        "details": diary.get("details"),
        "mood_score": diary.get("mood_score")
    }


@router.get("/diaries/{diary_id}")
async def get_diary(diary_id: int):
    """获取日记详情"""
    diaries = get_diaries(limit=100)
    diary = next((d for d in diaries if d.get("id") == diary_id), None)
    if not diary:
        raise HTTPException(status_code=404, detail="日记不存在")

    return {
        "id": diary.get("id"),
        "date": diary.get("date"),
        "summary": diary.get("summary"),
        "details": diary.get("details"),
        "mood_score": diary.get("mood_score")
    }


@router.put("/diaries/{diary_id}")
async def update_diary_entry(diary_id: int, entry: DiaryEntryUpdate):
    """更新日记"""
    # 先检查日记是否存在
    diaries = get_diaries(limit=100)
    existing = next((d for d in diaries if d.get("id") == diary_id), None)
    if not existing:
        raise HTTPException(status_code=404, detail="日记不存在")

    # 构建更新数据
    update_data = {}
    if entry.summary is not None:
        update_data["summary"] = entry.summary
    if entry.details is not None:
        update_data["details"] = entry.details
    if entry.mood_score is not None:
        update_data["mood_score"] = entry.mood_score

    diary = supabase_update_diary(diary_id, update_data)
    if not diary:
        raise HTTPException(status_code=404, detail="日记不存在")

    return {
        "id": diary.get("id"),
        "date": diary.get("date"),
        "summary": diary.get("summary"),
        "details": diary.get("details"),
        "mood_score": diary.get("mood_score")
    }


@router.delete("/diaries/{diary_id}")
async def delete_diary(diary_id: int):
    """删除日记"""
    from services.supabase_db import supabase as supabase_client

    # 检查日记是否存在
    diaries = get_diaries(limit=100)
    existing = next((d for d in diaries if d.get("id") == diary_id), None)
    if not existing:
        raise HTTPException(status_code=404, detail="日记不存在")

    # 删除日记
    supabase_client.table("diaries").delete().eq("id", diary_id).execute()

    return {"message": "日记已删除"}


@router.get("/diaries/date/{date_str}")
async def get_diary_by_date_str(date_str: str):
    """根据日期字符串获取日记"""
    # 验证日期格式
    try:
        from datetime import datetime
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="日期格式错误，请使用 YYYY-MM-DD")

    diary = get_diary_by_date(date_str)

    if not diary:
        return {
            "date": date_str,
            "summary": "今日暂无记录",
            "details": None,
            "mood_score": None
        }

    return {
        "id": diary.get("id"),
        "date": diary.get("date"),
        "summary": diary.get("summary"),
        "details": diary.get("details"),
        "mood_score": diary.get("mood_score")
    }