# 后端部署实现计划

> **面向 AI 代理的工作者：** 必需子技能：使用 superpowers:subagent-driven-development 逐任务实现此计划。

**目标：** 配置内网穿透，让手机在外网也能访问后端

**架构：** 使用 ngrok 将本地服务暴露到外网

**技术栈：** ngrok + FastAPI + Uvicorn

---

## 文件结构

| 文件 | 操作 | 说明 |
|------|------|------|
| `server/.env.example` | 修改 | 添加部署说明 |
| `docs/deployment-guide.md` | 创建 | 部署指南 |

---

## 任务

### 任务 1：创建部署指南

**文件：** 创建 `docs/deployment-guide.md`

- [ ] **步骤 1：创建部署指南**

```markdown
# SoundIOS 部署指南

## 开发环境部署

### 1. 启动后端服务

```bash
cd server
source venv/bin/activate
python main.py
```

后端运行在 http://localhost:8000

### 2. 测试 API

```bash
curl http://localhost:8000/health
```

## 外网访问（ngrok）

### 1. 安装 ngrok

```bash
# macOS
brew install ngrok

# 或下载安装
# https://ngrok.com/download
```

### 2. 配置认证

```bash
ngrok config add-authtoken YOUR_TOKEN
```

在 https://dashboard.ngrok.com/get-started/your-authtoken 获取 token

### 3. 启动隧道

```bash
ngrok http 8000
```

会显示类似：
```
Forwarding  https://xxxx-xx.ngrok-free.app -> http://localhost:8000
```

### 4. 更新 iOS 配置

在 `ios/SoundIOS/src/services/api.ts` 中：

```typescript
// 外网访问
const API_BASE_URL = 'https://xxxx-xx.ngrok-free.app/api';
```

## 生产环境注意事项

- 确保 Supabase 数据库 RLS 策略正确配置
- MiniMax API Key 不要暴露在前端
- 考虑使用云服务器替代本地开发
```

- [ ] **步骤 2：Commit**

```bash
git add docs/deployment-guide.md
git commit -m "docs: add deployment guide with ngrok"
```

---

### 任务 2：更新环境变量示例

**文件：** 修改 `server/.env.example`

- [ ] **步骤 1：更新 .env.example**

```bash
# MiniMax（STT + LLM + TTS）
MINIMAX_API_KEY=your-api-key

# Supabase 数据库
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key

# 服务器配置
HOST=0.0.0.0
PORT=8000

# ===== 部署说明 =====
# 开发环境：运行 python main.py
# 外网访问：使用 ngrok http 8000
```

- [ ] **步骤 2：Commit**

```bash
git add server/.env.example
git commit -m "docs: update .env.example with deployment notes"
```

---

### 任务 3：创建启动脚本

**文件：** 创建 `server/start.sh`

- [ ] **步骤 1：创建启动脚本**

```bash
#!/bin/bash
# SoundIOS 后端启动脚本

cd "$(dirname "$0")"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt --quiet

# 启动服务
echo "启动后端服务..."
python main.py
```

- [ ] **步骤 2：设置执行权限并 Commit**

```bash
chmod +x server/start.sh
git add server/start.sh
git commit -m "feat(deployment): add start script for backend"
```

---

## 验证

### 本地测试
```bash
cd server
./start.sh
curl http://localhost:8000/health
```

### ngrok 测试
```bash
ngrok http 8000
# 复制 Forwarding URL
# 在 iOS App 中使用该 URL 测试
```

预期：手机可以通过 ngrok URL 访问后端 API
