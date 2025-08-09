#!/bin/bash

echo "🔍 检查 Wellbeing Agent 应用状态..."
echo ""

# 检查 Node.js 进程
echo "📊 进程状态:"
if pgrep -f "npm run dev" > /dev/null; then
    echo "   ✅ 前端开发服务器: 运行中"
else
    echo "   ❌ 前端开发服务器: 未运行"
fi

# 检查端口占用
echo ""
echo "🌐 端口状态:"
if lsof -i :3000 > /dev/null 2>&1; then
    echo "   ✅ 端口 3000: 已占用 (前端服务)"
    PID=$(lsof -ti :3000)
    echo "       进程 ID: $PID"
else
    echo "   ❌ 端口 3000: 未占用"
fi

# 检查应用响应
echo ""
echo "📡 应用响应:"
if curl -s http://localhost:3000 > /dev/null; then
    echo "   ✅ 前端应用: 响应正常"
    echo "   🌐 访问地址: http://localhost:3000"
else
    echo "   ❌ 前端应用: 无响应"
fi

# 检查依赖状态
echo ""
echo "📦 依赖状态:"
if [ -d "node_modules" ]; then
    echo "   ✅ node_modules: 已安装"
    echo "   📋 依赖数量: $(ls node_modules | wc -l) 个包"
else
    echo "   ❌ node_modules: 未安装"
fi

# 检查配置文件
echo ""
echo "⚙️  配置文件:"
if [ -f "package.json" ]; then
    echo "   ✅ package.json: 存在"
    echo "   📋 项目名称: $(grep '"name"' package.json | cut -d'"' -f4)"
    echo "   📋 项目版本: $(grep '"version"' package.json | cut -d'"' -f4)"
else
    echo "   ❌ package.json: 不存在"
fi

if [ -f "vite.config.ts" ]; then
    echo "   ✅ vite.config.ts: 存在"
else
    echo "   ❌ vite.config.ts: 不存在"
fi

if [ -f "tailwind.config.js" ]; then
    echo "   ✅ tailwind.config.js: 存在"
else
    echo "   ❌ tailwind.config.js: 不存在"
fi

# 显示启动建议
echo ""
echo "🚀 启动建议:"
if ! pgrep -f "npm run dev" > /dev/null; then
    echo "   运行 './start_frontend.sh' 启动前端服务"
elif ! curl -s http://localhost:3000 > /dev/null; then
    echo "   前端服务可能正在启动中，请稍等..."
else
    echo "   🎉 应用运行正常！在浏览器中打开 http://localhost:3000"
fi

echo ""
echo "📚 更多信息请查看 FRONTEND_QUICKSTART.md"
