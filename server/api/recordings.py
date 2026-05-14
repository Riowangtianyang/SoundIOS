from fastapi import APIRouter, UploadFile, File, HTTPException
from services.supabase_db import (
    create_recording,
    get_recordings,
    get_recording,
    delete_recording,
    create_transcript,
    get_transcript,
)
from datetime import datetime
import os
import uuid

router = APIRouter()

UPLOAD_DIR = "./uploads"


@router.post("/recordings")
async def upload_recording(file: UploadFile = File(...)):
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

    recording = create_recording(audio_path=audio_path, duration=0.0)

    return {
        "id": recording.get("id"),
        "audio_path": recording.get("audio_path"),
        "status": recording.get("status"),
        "created_at": recording.get("created_at")
    }


@router.get("/recordings")
async def list_recordings():
    """获取录音列表"""
    recordings = get_recordings(limit=50)
    return {
        "recordings": [
            {
                "id": r.get("id"),
                "audio_path": r.get("audio_path"),
                "duration": r.get("duration"),
                "status": r.get("status"),
                "created_at": r.get("created_at")
            }
            for r in recordings
        ]
    }


@router.get("/recordings/{recording_id}")
async def get_recording_detail(recording_id: int):
    """获取录音详情"""
    recording = get_recording(recording_id)
    if not recording:
        raise HTTPException(status_code=404, detail="录音不存在")

    transcript = get_transcript(recording_id)

    return {
        "id": recording.get("id"),
        "audio_path": recording.get("audio_path"),
        "duration": recording.get("duration"),
        "status": recording.get("status"),
        "created_at": recording.get("created_at"),
        "transcript": {
            "text": transcript.get("text") if transcript else None,
            "segments": transcript.get("segments") if transcript else None
        } if transcript else None
    }


@router.delete("/recordings/{recording_id}")
async def delete_recording_api(recording_id: int):
    """删除录音"""
    recording = get_recording(recording_id)
    if not recording:
        raise HTTPException(status_code=404, detail="录音不存在")

    if os.path.exists(recording.get("audio_path", "")):
        os.remove(recording.get("audio_path"))

    delete_recording(recording_id)

    return {"message": "录音已删除"}