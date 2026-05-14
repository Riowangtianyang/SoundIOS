import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 测试环境使用临时文件数据库
_TESTING = os.environ.get("TESTING", "").lower() in ("1", "true", "yes")

if _TESTING:
    # 使用临时文件数据库
    import tempfile
    _db_file = os.path.join(tempfile.gettempdir(), "test_ai_memory.db")
    DATABASE_URL = f"sqlite:///{_db_file}"
else:
    from config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_engine():
    """获取数据库引擎"""
    return engine


def init_db():
    """初始化数据库，创建所有表"""
    from models.database import Recording, Transcript, DiaryEntry, Todo, Person, Memory
    Base.metadata.create_all(bind=engine)