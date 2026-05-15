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