"""
后端服务测试用例
测试 API 端点功能
"""
import pytest
import os

# 设置测试环境 - 必须在任何其他导入之前
os.environ["TESTING"] = "1"

# 首先创建数据库表
from models import Base, engine, SessionLocal
from models.database import Recording, Transcript, DiaryEntry, Todo, Person, Memory

# 确保所有模型类被导入，然后创建表
Base.metadata.create_all(bind=engine)

# 最后导入 app 和 client
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestHealthEndpoint:
    """健康检查接口测试"""

    def test_root_endpoint(self):
        """测试根路径返回正确信息"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

    def test_health_check(self):
        """测试健康检查接口"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestRecordingsAPI:
    """录音 API 测试"""

    def test_list_recordings_empty(self):
        """测试空录音列表"""
        response = client.get("/api/recordings")
        assert response.status_code == 200
        data = response.json()
        assert "recordings" in data

    def test_get_nonexistent_recording(self):
        """测试获取不存在的录音"""
        response = client.get("/api/recordings/999999")
        assert response.status_code in [404, 500]


class TestTodosAPI:
    """待办 API 测试"""

    def test_list_todos_empty(self):
        """测试空待办列表"""
        response = client.get("/api/todos")
        assert response.status_code == 200
        data = response.json()
        assert "todos" in data

    def test_create_todo(self):
        """测试创建待办"""
        todo_data = {
            "title": "测试待办",
            "description": "这是一个测试待办",
            "priority": 2
        }
        response = client.post("/api/todos", json=todo_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == todo_data["title"]
        return data.get("id")

    def test_update_todo_status(self):
        """测试更新待办状态"""
        todo_id = self.test_create_todo()
        if todo_id:
            response = client.put(f"/api/todos/{todo_id}", json={"status": "completed"})
            assert response.status_code == 200

    def test_delete_todo(self):
        """测试删除待办"""
        todo_id = self.test_create_todo()
        if todo_id:
            response = client.delete(f"/api/todos/{todo_id}")
            assert response.status_code == 200


class TestDiaryAPI:
    """日记 API 测试"""

    def test_list_diaries_empty(self):
        """测试空日记列表"""
        response = client.get("/api/diaries")
        assert response.status_code == 200

    def test_get_diary_by_date(self):
        """测试获取指定日期日记"""
        response = client.get("/api/diaries/date/2026-05-14")
        assert response.status_code == 200


class TestPersonsAPI:
    """人物 API 测试"""

    def test_list_persons_empty(self):
        """测试空人物列表"""
        response = client.get("/api/persons")
        assert response.status_code == 200
        data = response.json()
        assert "persons" in data

    def test_create_person(self):
        """测试创建人物"""
        person_data = {
            "name": "测试人物",
            "relationship_type": "同事",
            "notes": "测试备注"
        }
        response = client.post("/api/persons", json=person_data)
        assert response.status_code == 200


class TestChatAPI:
    """问AI API 测试"""

    def test_chat_endpoint_exists(self):
        """测试聊天接口存在"""
        response = client.post("/api/chat", json={"messages": [{"role": "user", "content": "你好"}]})
        assert response.status_code == 200

    def test_chat_context(self):
        """测试获取聊天上下文"""
        response = client.get("/api/chat/context")
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
