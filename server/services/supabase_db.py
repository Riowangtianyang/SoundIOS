"""
Supabase Database Service
Supabase 数据库服务封装
"""
from supabase import create_client, Client
import os

# 初始化 Supabase 客户端
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

_supabase_client: Client = None


def get_supabase() -> Client:
    """获取 Supabase 客户端单例"""
    global _supabase_client
    if _supabase_client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _supabase_client


# ============ Person Operations ============

def create_person(name: str, relationship_type: str = None, notes: str = None, personality_tags: list = None):
    """创建人物"""
    supabase = get_supabase()
    data = {
        "name": name,
        "relationship_type": relationship_type,
        "notes": notes,
        "personality_tags": personality_tags or [],
        "interaction_count": 0
    }
    result = supabase.table("persons").insert(data).execute()
    return result.data[0] if result.data else None


def get_persons():
    """获取所有人物"""
    supabase = get_supabase()
    result = supabase.table("persons").select("*").execute()
    return result.data


def get_person(id: int):
    """获取单个人物"""
    supabase = get_supabase()
    result = supabase.table("persons").select("*").eq("id", id).execute()
    return result.data[0] if result.data else None


def update_person(id: int, data: dict):
    """更新人物信息"""
    supabase = get_supabase()
    result = supabase.table("persons").update(data).eq("id", id).execute()
    return result.data[0] if result.data else None


def increment_person_interaction(id: int):
    """增加人物互动次数"""
    supabase = get_supabase()
    # 先获取当前值
    person = get_person(id)
    if not person:
        return None
    new_count = (person.get("interaction_count") or 0) + 1
    result = supabase.table("persons").update({"interaction_count": new_count}).eq("id", id).execute()
    return result.data[0] if result.data else None


def delete_person(id: int):
    """删除人物"""
    supabase = get_supabase()
    supabase.table("persons").delete().eq("id", id).execute()
    return True


# ============ Memory Operations ============

def create_memory(content: str, person_id: int = None, category: str = None, confirmed: int = 0):
    """创建记忆"""
    supabase = get_supabase()
    data = {
        "content": content,
        "person_id": person_id,
        "category": category,
        "confirmed": confirmed
    }
    result = supabase.table("memories").insert(data).execute()
    return result.data[0] if result.data else None


def get_memories(person_id: int = None, confirmed: int = None):
    """获取记忆列表"""
    supabase = get_supabase()
    query = supabase.table("memories").select("*")
    if person_id is not None:
        query = query.eq("person_id", person_id)
    if confirmed is not None:
        query = query.eq("confirmed", confirmed)
    result = query.execute()
    return result.data


def update_memory_confirmed(id: int, confirmed: int):
    """更新记忆确认状态"""
    supabase = get_supabase()
    result = supabase.table("memories").update({"confirmed": confirmed}).eq("id", id).execute()
    return result.data[0] if result.data else None


# ============ Todo Operations ============

def create_todo(
    title: str,
    description: str = None,
    due_date: str = None,
    priority: int = 3,
    status: str = "pending",
    source_recording_id: int = None
):
    """创建待办事项"""
    supabase = get_supabase()
    data = {
        "title": title,
        "description": description,
        "due_date": due_date,
        "priority": priority,
        "status": status
    }
    if source_recording_id:
        data["source_recording_id"] = source_recording_id
    result = supabase.table("todos").insert(data).execute()
    return result.data[0] if result.data else None


def get_todos(status: str = None, limit: int = 100):
    """获取待办事项列表"""
    supabase = get_supabase()
    query = supabase.table("todos").select("*")
    if status:
        query = query.eq("status", status)
    # 按 priority 升序, due_date 升序排序
    result = query.order("priority", desc=False).order("due_date", desc=False).limit(limit).execute()
    return result.data or []


def get_todo(id: int):
    """获取单个待办事项"""
    supabase = get_supabase()
    result = supabase.table("todos").select("*").eq("id", id).execute()
    return result.data[0] if result.data else None


def update_todo(id: int, data: dict):
    """更新待办事项"""
    supabase = get_supabase()
    result = supabase.table("todos").update(data).eq("id", id).execute()
    return result.data[0] if result.data else None


def delete_todo(id: int):
    """删除待办事项"""
    supabase = get_supabase()
    supabase.table("todos").delete().eq("id", id).execute()
    return True