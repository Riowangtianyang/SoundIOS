"""
pytest 配置（使用 Supabase）
"""
import os

# 设置测试环境
os.environ["TESTING"] = "1"

import pytest
from unittest.mock import MagicMock, patch

# Mock Supabase 客户端
mock_client = MagicMock()
mock_client.table = MagicMock(return_value=MagicMock(
    select=MagicMock(return_value=MagicMock(
        execute=MagicMock(return_value=MagicMock(data=[]))
    ))
))

@pytest.fixture(scope="session", autouse=True)
def setup_mock_supabase():
    """Mock Supabase 客户端"""
    with patch("services.supabase_db.create_client", return_value=mock_client):
        yield