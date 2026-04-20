#!/bin/bash

# 自动部署脚本
# 使用方法: ./deploy.sh "提交信息"

set -e

# 检查是否在 git 仓库中
if [ ! -d ".git" ]; then
    echo "❌ 错误: 当前目录不是 git 仓库"
    exit 1
fi

# 获取提交信息
COMMIT_MSG=${1:-"更新网站内容"}

# 检查 Git 状态
echo "📋 检查 Git 状态..."
git status

# 添加所有更改
echo "📦 添加更改..."
git add .

# 检查是否有更改需要提交
if git diff --cached --quiet; then
    echo "ℹ️ 没有需要提交的更改"
    exit 0
fi

# 提交更改
echo "✅ 提交更改: $COMMIT_MSG"
git commit -m "$COMMIT_MSG"

# 推送到远程仓库
echo "🚀 推送到 GitHub..."
git push origin new-personal-homepage

echo "✨ 部署完成！"
