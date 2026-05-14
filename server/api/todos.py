from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models import get_db
from models.database import Todo

router = APIRouter()


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[int] = 3
    status: Optional[str] = "pending"


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[int] = None
    status: Optional[str] = None


@router.get("/todos")
async def list_todos(
    status: Optional[str] = None,
    priority: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """获取待办列表"""
    query = db.query(Todo)

    if status:
        query = query.filter(Todo.status == status)
    if priority is not None:
        query = query.filter(Todo.priority == priority)

    todos = query.order_by(Todo.priority.asc(), Todo.due_date.asc()).all()

    return {
        "todos": [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "due_date": t.due_date,
                "priority": t.priority,
                "status": t.status
            }
            for t in todos
        ]
    }


@router.post("/todos")
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """创建待办"""
    new_todo = Todo(
        title=todo.title,
        description=todo.description,
        due_date=todo.due_date,
        priority=todo.priority or 3,
        status=todo.status or "pending"
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return {
        "id": new_todo.id,
        "title": new_todo.title,
        "description": new_todo.description,
        "due_date": new_todo.due_date,
        "priority": new_todo.priority,
        "status": new_todo.status
    }


@router.get("/todos/{todo_id}")
async def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """获取待办详情"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="待办不存在")

    return {
        "id": todo.id,
        "title": todo.title,
        "description": todo.description,
        "due_date": todo.due_date,
        "priority": todo.priority,
        "status": todo.status
    }


@router.put("/todos/{todo_id}")
async def update_todo(todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_db)):
    """更新待办"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="待办不存在")

    if todo_update.title is not None:
        todo.title = todo_update.title
    if todo_update.description is not None:
        todo.description = todo_update.description
    if todo_update.due_date is not None:
        todo.due_date = todo_update.due_date
    if todo_update.priority is not None:
        todo.priority = todo_update.priority
    if todo_update.status is not None:
        todo.status = todo_update.status

    db.commit()
    db.refresh(todo)

    return {
        "id": todo.id,
        "title": todo.title,
        "description": todo.description,
        "due_date": todo.due_date,
        "priority": todo.priority,
        "status": todo.status
    }


@router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """删除待办"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="待办不存在")

    db.delete(todo)
    db.commit()

    return {"message": "待办已删除"}