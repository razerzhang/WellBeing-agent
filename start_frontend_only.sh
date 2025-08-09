#!/bin/bash

# 前端启动脚本（从根目录运行）
echo "🚀 启动 Wellbeing Agent 前端应用..."

# 检查前端目录是否存在
if [ ! -d "frontend" ]; then
    echo "❌ 错误：frontend 目录不存在"
    exit 1
fi

# 进入前端目录并启动
cd frontend
./start.sh
