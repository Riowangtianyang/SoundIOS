"""
pytest 配置
"""
import os

# 在任何导入前设置测试环境
os.environ["TESTING"] = "1"

import pytest

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """初始化测试数据库"""
    from models import Base, get_engine
    from models.database import Recording, Transcript, DiaryEntry, Todo, Person, Memory
    
    engine = get_engine()
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    yield
    # 清理
    Base.metadata.drop_all(bind=engine)
