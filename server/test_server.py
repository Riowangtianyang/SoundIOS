"""
后端服务测试用例
测试 API 端点功能（使用 Supabase）
"""
import pytest
import os
from unittest.mock import MagicMock, patch

# 设置测试环境
os.environ["TESTING"] = "1"

# Mock Supabase 客户端
mock_client = MagicMock()
mock_client.table = MagicMock(return_value=MagicMock(
    select=MagicMock(return_value=MagicMock(
        execute=MagicMock(return_value=MagicMock(data=[]))
    ))
))

# 在导入 app 前 mock supabase
with patch("services.supabase_db.create_client", return_value=mock_client):
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

    def test_list_recordings(self):
        """测试录音列表"""
        response = client.get("/api/recordings")
        assert response.status_code == 200
        data = response.json()
        assert "recordings" in data


class TestTodosAPI:
    """待办 API 测试"""

    def test_list_todos(self):
        """测试待办列表"""
        response = client.get("/api/todos")
        assert response.status_code == 200
        data = response.json()
        assert "todos" in data


class TestDiaryAPI:
    """日记 API 测试"""

    def test_list_diaries(self):
        """测试日记列表"""
        response = client.get("/api/diaries")
        assert response.status_code == 200

    def test_get_diary_by_date(self):
        """测试获取指定日期日记"""
        response = client.get("/api/diaries/date/2026-05-14")
        assert response.status_code == 200


class TestPersonsAPI:
    """人物 API 测试"""

    def test_list_persons(self):
        """测试人物列表"""
        response = client.get("/api/persons")
        assert response.status_code == 200
        data = response.json()
        assert "persons" in data


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