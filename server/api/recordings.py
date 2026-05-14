from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from models import get_db
from models.database import Recording
from datetime import datetime
import os
import uuid

router = APIRouter()

UPLOAD_DIR = "./uploads"


@router.post("/recordings")
async def upload_recording(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """上传录音文件"""
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_id = str(uuid.uuid4())
    file_extension = os.path.splitext(file.filename)[1] if file.filename else ".m4a"
    audio_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_extension}")

    try:
        with open(audio_path, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存文件失败: {str(e)}")

    recording = Recording(
        audio_path=audio_path,
        status="pending"
    )
    db.add(recording)
    db.commit()
    db.refresh(recording)

    return {
        "id": recording.id,
        "audio_path": recording.audio_path,
        "status": recording.status,
        "created_at": recording.created_at
    }


@router.get("/recordings")
async def list_recordings(db: Session = Depends(get_db)):
    """获取录音列表"""
    recordings = db.query(Recording).order_by(Recording.created_at.desc()).all()
    return {
        "recordings": [
            {
                "id": r.id,
                "audio_path": r.audio_path,
                "duration": r.duration,
                "status": r.status,
                "created_at": r.created_at
            }
            for r in recordings
        ]
    }


@router.get("/recordings/{recording_id}")
async def get_recording(recording_id: int, db: Session = Depends(get_db)):
    """获取录音详情"""
    recording = db.query(Recording).filter(Recording.id == recording_id).first()
    if not recording:
        raise HTTPException(status_code=404, detail="录音不存在")

    return {
        "id": recording.id,
        "audio_path": recording.audio_path,
        "duration": recording.duration,
        "status": recording.status,
        "created_at": recording.created_at,
        "transcript": {
            "text": recording.transcript.text if recording.transcript else None,
            "segments": recording.transcript.segments if recording.transcript else None
        } if recording.transcript else None
    }


@router.delete("/recordings/{recording_id}")
async def delete_recording(recording_id: int, db: Session = Depends(get_db)):
    """删除录音"""
    recording = db.query(Recording).filter(Recording.id == recording_id).first()
    if not recording:
        raise HTTPException(status_code=404, detail="录音不存在")

    if os.path.exists(recording.audio_path):
        os.remove(recording.audio_path)

    db.delete(recording)
    db.commit()

    return {"message": "录音已删除"}