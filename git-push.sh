#!/bin/bash
# AI 个人记忆助手 - 一键提交推送脚本
# 用途：自动添加文件、提交、推送到 GitHub

set -e

PROJECT_DIR="/Users/wangyang/Documents/GitHub/Personal/SoundIOS"
cd "$PROJECT_DIR"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  AI 个人记忆助手 - Git 提交推送${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 读取提交信息（如果没提供参数）
if [ -z "$1" ]; then
    echo "📝 请输入提交描述（按回车确认）："
    read -r commit_msg
    if [ -z "$commit_msg" ]; then
        commit_msg="更新: $(date '+%Y-%m-%d %H:%M')"
    fi
else
    commit_msg="$1"
fi

echo -e "${YELLOW}📦 添加文件...${NC}"
git add .

echo -e "${YELLOW}💾 提交中: ${commit_msg}${NC}"
git commit -m "$commit_msg"

echo -e "${YELLOW}🚀 推送到 GitHub...${NC}"
git push

echo ""
echo -e "${GREEN}✅ 完成！${NC}"
echo -e "${GREEN}🌐 仓库：https://github.com/boos/SoundIOS${NC}"
echo ""