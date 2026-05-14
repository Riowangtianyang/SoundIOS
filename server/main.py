from fastapi import FastAPI
from api import recordings, diary, todos, persons, chat

app = FastAPI(title="AI Memory Assistant API", version="1.0.0")

# 注册路由（Supabase 在 supabase_db.py 中按需初始化）
app.include_router(recordings.router, prefix="/api", tags=["recordings"])
app.include_router(diary.router, prefix="/api", tags=["diary"])
app.include_router(todos.router, prefix="/api", tags=["todos"])
app.include_router(persons.router, prefix="/api", tags=["persons"])
app.include_router(chat.router, prefix="/api", tags=["chat"])


@app.get("/")
async def root():
    return {"message": "AI Memory Assistant API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
