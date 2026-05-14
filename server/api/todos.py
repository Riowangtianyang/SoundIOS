from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.supabase_db import (
    create_todo as supabase_create_todo,
    get_todos,
    get_todo as supabase_get_todo,
    update_todo as supabase_update_todo,
    delete_todo as supabase_delete_todo
)

router = APIRouter()


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[str] = None
    priority: Optional[int] = 3
    status: Optional[str] = "pending"


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None
    priority: Optional[int] = None
    status: Optional[str] = None


@router.get("/todos")
async def list_todos(
    status: Optional[str] = None,
    priority: Optional[int] = None
):
    """获取待办列表"""
    todos = get_todos(status=status)

    # 内存中过滤 priority（保持与原 API 一致的行为）
    if priority is not None:
        todos = [t for t in todos if t.get("priority") == priority]

    return {
        "todos": [
            {
                "id": t.get("id"),
                "title": t.get("title"),
                "description": t.get("description"),
                "due_date": t.get("due_date"),
                "priority": t.get("priority"),
                "status": t.get("status")
            }
            for t in todos
        ]
    }


@router.post("/todos")
async def create_todo(todo: TodoCreate):
    """创建待办"""
    new_todo = supabase_create_todo(
        title=todo.title,
        description=todo.description,
        due_date=todo.due_date,
        priority=todo.priority or 3,
        status=todo.status or "pending"
    )

    return {
        "id": new_todo.get("id"),
        "title": new_todo.get("title"),
        "description": new_todo.get("description"),
        "due_date": new_todo.get("due_date"),
        "priority": new_todo.get("priority"),
        "status": new_todo.get("status")
    }


@router.get("/todos/{todo_id}")
async def get_todo(todo_id: int):
    """获取待办详情"""
    todo = supabase_get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="待办不存在")

    return {
        "id": todo.get("id"),
        "title": todo.get("title"),
        "description": todo.get("description"),
        "due_date": todo.get("due_date"),
        "priority": todo.get("priority"),
        "status": todo.get("status")
    }


@router.put("/todos/{todo_id}")
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    """更新待办"""
    # 检查待办是否存在
    existing = supabase_get_todo(todo_id)
    if not existing:
        raise HTTPException(status_code=404, detail="待办不存在")

    # 构建更新数据
    update_data = {}
    if todo_update.title is not None:
        update_data["title"] = todo_update.title
    if todo_update.description is not None:
        update_data["description"] = todo_update.description
    if todo_update.due_date is not None:
        update_data["due_date"] = todo_update.due_date
    if todo_update.priority is not None:
        update_data["priority"] = todo_update.priority
    if todo_update.status is not None:
        update_data["status"] = todo_update.status

    todo = supabase_update_todo(todo_id, update_data)

    return {
        "id": todo.get("id"),
        "title": todo.get("title"),
        "description": todo.get("description"),
        "due_date": todo.get("due_date"),
        "priority": todo.get("priority"),
        "status": todo.get("status")
    }


@router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    """删除待办"""
    # 检查待办是否存在
    existing = supabase_get_todo(todo_id)
    if not existing:
        raise HTTPException(status_code=404, detail="待办不存在")

    supabase_delete_todo(todo_id)

    return {"message": "待办已删除"}