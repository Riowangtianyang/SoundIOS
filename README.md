# SoundIOS - AI 个人记忆助手

基于手机录音 + AI 分析的个人记忆系统。自动记录现实对话，转写、分析、提取待办、建立人物关系。

## 功能特性

- 🎙 **智能录音** - 自动检测语音并分段记录
- 📝 **AI 日记** - 自动生成每日摘要和分析
- ✅ **待办提取** - 从对话中智能提取待办事项
- 👥 **人物关系** - 知识图谱可视化人脉网络
- 💬 **问 AI** - 用自然语言查询你的记忆

## 技术栈

- 📱 **iOS App**: React Native + TypeScript
- 🖥️ **后端服务**: Python FastAPI
- 🔊 **STT**: 腾讯云 ASR
- 🤖 **LLM**: MiniMax

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/Riowangtianyang/SoundIOS.git
cd SoundIOS
```

### 2. 配置 API 密钥

```bash
cd server
cp .env.example .env
# 编辑 .env 填入你的密钥
```

需要以下密钥：
- **腾讯云 ASR**: https://console.cloud.tencent.com/cam/capi
- **MiniMax**: https://platform.minimax.chat/

### 3. 启动后端服务

```bash
cd server
pip install -r requirements.txt
python main.py
```

服务运行在 http://localhost:8000

### 4. iOS App（开发中）

```bash
cd ios
npm install
npx react-native run-ios
```

## 项目结构

```
SoundIOS/
├── ios/                    # React Native App
│   └── src/
│       ├── screens/        # 页面组件
│       ├── services/       # API 服务
│       └── theme/          # 设计系统
├── server/                 # Python 后端
│   ├── api/               # API 路由
│   ├── services/          # AI 服务
│   └── models/            # 数据库模型
└── docs/                  # 设计文档
```

## 设计系统

Neural Warmth - 温暖神经网络风格

- 深色背景 + 琥珀主色
- 节点图谱可视化
- 流畅的微交互动画

## License

MIT