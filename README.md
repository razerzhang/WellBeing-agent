# Wellbeing Agent - 智能健康顾问

一个基于 LangGraph 和 React 的智能健康顾问系统，提供个性化的健康建议和运动指导。

## 🏗️ 项目结构

```
langgraph-agent/
├── frontend/              # 前端应用 (React + TypeScript)
│   ├── src/              # React 源代码
│   ├── package.json      # 前端依赖配置
│   └── start.sh          # 前端启动脚本
├── server.py             # 后端 API 服务器
├── wellbeing_agent.py    # 核心健康顾问代理
├── deepseek_llm.py      # DeepSeek LLM 集成
├── requirements.txt      # Python 依赖
└── start_server.py       # 后端启动脚本
```

## 🚀 快速开始

### 1. 启动后端服务

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 启动后端服务器
python start_server.py
```

### 2. 启动前端应用

```bash
# 方法1：使用启动脚本
./start_frontend_only.sh

# 方法2：手动启动
cd frontend
npm install
npm run dev
```

### 3. 访问应用

- 前端应用: http://localhost:3000
- 后端 API: http://localhost:8000

## 🛠️ 技术架构

### 后端
- **LangGraph** - 代理编排框架
- **FastAPI** - 高性能 Web API 框架
- **DeepSeek** - 大语言模型集成
- **Python 3.8+** - 核心开发语言

### 前端
- **React 18** - 用户界面库
- **TypeScript** - 类型安全的 JavaScript
- **Tailwind CSS** - 实用优先的 CSS 框架
- **Vite** - 快速的前端构建工具

## 🎯 核心功能

- **智能健康咨询** - 基于 AI 的健康建议
- **运动指导** - 个性化运动计划
- **饮食建议** - 营养搭配指导
- **健康管理** - 生活方式优化
- **流式输出** - 实时响应体验

## 📁 目录说明

### 前端 (`frontend/`)
- 完全独立的前端应用
- 使用现代 React 技术栈
- 支持热重载和快速开发

### 后端 (根目录)
- LangGraph 代理系统
- FastAPI 服务器
- 健康顾问核心逻辑

## 🔧 开发说明

### 前端开发
```bash
cd frontend
npm run dev          # 启动开发服务器
npm run build        # 构建生产版本
npm run preview      # 预览生产版本
```

### 后端开发
```bash
python start_server.py    # 启动开发服务器
python -m pytest         # 运行测试
```

## 📚 文档

- [前端快速开始](frontend/README.md)
- [API 文档](DEMO.md)
- [流式输出说明](STREAMING_README.md)
- [实现总结](IMPLEMENTATION_SUMMARY.md)

## 🚀 部署

### 前端部署
前端应用可以部署到任何静态文件托管服务：
- Vercel, Netlify, GitHub Pages
- AWS S3 + CloudFront

### 后端部署
- Docker 容器化
- 云服务器部署
- 支持环境变量配置

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## �� 许可证

MIT License
