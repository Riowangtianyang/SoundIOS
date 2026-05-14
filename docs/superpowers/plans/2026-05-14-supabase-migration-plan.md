# SoundIOS Supabase 迁移实现计划

> **面向 AI 代理的工作者：** 必需子技能：使用 superpowers:subagent-driven-development（推荐）或 superpowers:executing-plans 逐任务实现此计划。步骤使用复选框（`- [ ]`）语法来跟踪进度。

**目标：** 将后端从 SQLite 完全迁移到 Supabase

**架构：** 删除 SQLAlchemy 相关代码，API 路由改用 supabase_db.py 直接操作 Supabase

**技术栈：** Python FastAPI, Supabase Python SDK

---

## 文件结构

| 文件 | 操作 | 说明 |
|------|------|------|
| `server/models/__init__.py` | 删除 | SQLAlchemy 初始化 |
| `server/models/database.py` | 删除 | ORM 模型定义 |
| `server/ai_memory.db*` | 删除 | SQLite 数据库 |
| `server/main.py` | 修改 | 移除 SQLAlchemy 初始化 |
| `server/api/recordings.py` | 修改 | 改用 supabase_db |
| `server/api/todos.py` | 修改 | 改用 supabase_db |
| `server/api/diary.py` | 修改 | 改用 supabase_db |
| `server/api/persons.py` | 修改 | 改用 supabase_db |
| `server/api/chat.py` | 修改 | 改用 supabase_db |
| `server/.env.example` | 修改 | 添加 Supabase 配置说明 |

---

## 实施步骤

### 任务 1：删除 models/ 目录

```bash
cd /Users/wangyang/Documents/GitHub/Personal/SoundIOS/server
rm -f ai_memory.db ai_memory.db-journal
rm -rf models/
```

### 任务 2：更新 main.py

移除 SQLAlchemy 初始化，保留路由注册。

### 任务 3-7：重写 API 路由

5 个文件统一替换：移除 SQLAlchemy 依赖 → 改用 supabase_db.py

### 任务 8：更新 .env.example

添加 SUPABASE_URL 和 SUPABASE_KEY 配置项

---

## 验证

```bash
cd /Users/wangyang/Documents/GitHub/Personal/SoundIOS/server
python -c "from services.supabase_db import get_supabase; print('OK')"
curl http://localhost:8000/health
```
