#!/bin/bash
# AI 个人记忆助手 - Git 初始化脚本
# 自动设置 Git 仓库并推送到 GitHub

set -e

PROJECT_DIR="/Users/wangyang/Documents/GitHub/Personal/SoundIOS"
cd "$PROJECT_DIR"

echo ""
echo "=========================================="
echo "  AI 个人记忆助手 - Git 初始化"
echo "=========================================="
echo ""

# 检查是否已有 Git 仓库
if [ -d ".git" ]; then
    echo "✅ Git 仓库已存在"
else
    echo "📦 初始化 Git 仓库..."
    git init
fi

# 设置默认分支为 main
git branch -M main

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
.pytest_cache/
.coverage
htmlcov/

# Virtual environments
venv/
ENV/

# Byte-compiled
__pycache__/
*.py[cod]

# Virtual environment
venv/
ENV/
EOF

# 添加远程仓库
echo "🔗 设置远程仓库..."
if ! git remote -v | grep -q origin; then
    git remote add origin https://github.com/boos/SoundIOS.git
fi

# 添加文件
echo "📦 添加文件到暂存区..."
git add .

# 检查是否有内容提交
if git diff --cached --quiet; then
    echo "⚠️  没有文件需要提交（可能已被忽略）"
else
    # 提交
    echo "💾 提交代码..."
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

    # 推送到 GitHub
    echo ""
    echo "🚀 推送到 GitHub..."
    git push -u origin main --force

    echo ""
    echo "=========================================="
    echo "✅ 完成！"
    echo "🌐 仓库地址：https://github.com/boos/SoundIOS"
    echo "=========================================="
fi

echo ""
echo "📊 项目结构："
echo "├── ios/          # React Native App"
echo "├── server/       # Python 后端服务"
echo "├── docs/         # 设计文档"
echo "└── 个人助手app/  # 其他文件"
echo ""