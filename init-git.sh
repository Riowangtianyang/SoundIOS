#!/bin/bash
# GitHub 仓库初始化脚本

PROJECT_DIR="/Users/wangyang/Documents/GitHub/Personal/SoundIOS"
cd "$PROJECT_DIR"

echo "📦 AI 个人记忆助手 - Git 初始化脚本"
echo "=========================================="

# 检查是否已有 git 仓库
if [ -d ".git" ]; then
    echo "⚠️  Git 仓库已存在，跳过初始化"
else
    echo "🔧 初始化 Git 仓库..."
    git init
fi

# 创建 .gitignore
echo "📝 创建 .gitignore..."
cat > .gitignore << 'EOF'
# Dependencies
node_modules/
.pnp
.pnp.js

# Build outputs
build/
dist/
*.apk
*.aab
*.apks
*.bundle

# iOS
ios/Pods/
ios/build/
ios/*.xcworkspace
ios/*.xcodeproj
*.dSYM.zip
*.hmap

# Android
android/app/build/
android/build/
android/.gradle/
*.keystore

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*
*.log

# macOS
.DS_Store
*.pem

# Local env files
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.idea/
.vscode/
*.swp
*.swo

# Testing
coverage/

# Database
*.db
*.db-journal

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/
dist/
build/

# Byte-compiled / optimized
__pycache__/

# Test
.pytest_cache/
.coverage
htmlcov/

# Virtual environments
venv/
ENV/
EOF

# 检查远程仓库是否已添加
REMOTE_CHECK=$(git remote -v 2>/dev/null | grep origin)
if [ -z "$REMOTE_CHECK" ]; then
    echo "🔗 添加远程仓库..."
    git remote add origin https://github.com/boos/SoundIOS.git
else
    echo "🔗 远程仓库已存在"
fi

# 创建 main 分支并切换
echo "🌿 创建 main 分支..."
git branch -M main

# 添加 .gitignore
git add .gitignore
git commit -m "chore: add .gitignore" 2>/dev/null || true

# 添加所有项目文件
echo "📦 添加项目文件..."
git add .

# 创建提交
echo "💾 创建提交..."
git commit -m "✨ AI 个人记忆助手 - 初始版本

📱 iOS App (React Native)
├── 首页：录音控制 + 实时状态
├── 日记：每日摘要 + 周统计
├── 待办：任务管理 + 来源追踪
├── 人物：知识图谱可视化
└── 问AI：对话查询 + 快捷问题

🖥️ 后端服务 (Python FastAPI)
├── 录音 API：上传/列表/转写
├── 日记 API：CRUD + 按日期查询
├── 待办 API：CRUD + 状态管理
├── 人物 API：CRUD + 关系管理
├── 问AI API：对话 + 上下文
├── STT 集成：腾讯云 ASR
└── LLM 集成：MiniMax

🎨 设计系统：Neural Warmth
├── 深色背景 + 琥珀主色
├── 知识图谱可视化
└── 节点关系网络"

# 推送代码
echo ""
echo "🚀 推送到 GitHub..."
git push -u origin main --force

echo ""
echo "=========================================="
echo "✅ 完成！"
echo "🌐 仓库地址：https://github.com/boos/SoundIOS"
echo ""
echo "📊 项目结构："
echo "├── ios/          # React Native App"
echo "├── server/       # Python 后端服务"
echo "├── docs/         # 设计文档"
echo "└── 个人助手app/  # 其他文件"