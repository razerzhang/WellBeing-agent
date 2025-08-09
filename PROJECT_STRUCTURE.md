# Wellbeing Agent 项目结构

## 📁 目录组织

```
langgraph-agent/
├── frontend/                    # 🎨 前端应用 (完全独立)
│   ├── src/                    # React 源代码
│   │   ├── components/         # React 组件
│   │   │   ├── ChatInterface.tsx
│   │   │   └── Sidebar.tsx
│   │   ├── App.tsx            # 主应用组件
│   │   ├── main.tsx           # 应用入口点
│   │   ├── types.ts           # TypeScript 类型定义
│   │   └── index.css          # 全局样式
│   ├── index.html              # HTML 入口文件
│   ├── package.json            # 前端依赖配置
│   ├── package-lock.json       # 依赖锁定文件
│   ├── tsconfig.json           # TypeScript 配置
│   ├── tsconfig.node.json      # Node.js TypeScript 配置
│   ├── vite.config.ts          # Vite 构建配置
│   ├── tailwind.config.js      # Tailwind CSS 配置
│   ├── postcss.config.js       # PostCSS 配置
│   ├── start.sh               # 前端启动脚本
│   ├── README.md               # 前端文档
│   ├── node_modules/           # 前端依赖包
│   ├── styles.css              # 传统 CSS 样式 (保留)
│   └── script.js               # 传统 JS 逻辑 (保留)
│
├── server.py                   # 🚀 后端 API 服务器
├── wellbeing_agent.py          # 🤖 核心健康顾问代理
├── deepseek_llm.py            # 🧠 DeepSeek LLM 集成
├── advanced_agent.py           # 🔧 高级代理功能
├── main.py                     # 📱 主程序入口
├── run.py                      # 🏃 运行脚本
├── setup.py                    # ⚙️ 安装配置
├── requirements.txt            # 🐍 Python 依赖
├── start_server.py             # 🚀 后端启动脚本
├── start_all.py                # 🔄 全栈启动脚本
├── start_frontend.sh           # 🎨 前端启动脚本 (旧版)
├── start_frontend_only.sh      # 🎨 前端启动脚本 (新版)
├── check_status.sh             # 📊 状态检查脚本
│
├── test_agent.py               # 🧪 代理测试
├── test_streaming.py           # 🧪 流式输出测试
├── test_streaming_wellbeing.py # 🧪 健康代理流式测试
├── example.py                  # 📝 使用示例
│
├── README.md                   # 📚 项目主文档
├── DEMO.md                     # 🎬 演示说明
├── QUICKSTART.md               # 🚀 快速开始
├── FRONTEND_QUICKSTART.md      # 🎨 前端快速开始
├── IMPLEMENTATION_SUMMARY.md   # 📋 实现总结
├── STREAMING_README.md         # 🌊 流式输出说明
├── PROJECT_STRUCTURE.md        # 📁 项目结构说明 (本文件)
│
├── .gitignore                  # 🚫 Git 忽略文件
└── venv/                       # 🐍 Python 虚拟环境
```

## 🔄 重构总结

### ✅ 已完成的重构

1. **前端代码完全分离**
   - 所有前端相关文件移动到 `frontend/` 目录
   - 包括 React 源代码、配置文件、依赖包等

2. **配置文件重新组织**
   - `package.json` → `frontend/package.json`
   - `vite.config.ts` → `frontend/vite.config.ts`
   - `tailwind.config.js` → `frontend/tailwind.config.js`
   - `tsconfig.json` → `frontend/tsconfig.json`

3. **启动脚本优化**
   - 创建 `frontend/start.sh` 前端专用启动脚本
   - 创建 `start_frontend_only.sh` 根目录前端启动脚本
   - 保留原有的全栈启动脚本

4. **文档更新**
   - 更新根目录 `README.md`
   - 更新前端目录 `README.md`
   - 创建项目结构说明文档

### 🎯 重构目标达成

- ✅ 前端代码完全独立，不与 Python 代码混在一起
- ✅ 保持原有的功能完整性
- ✅ 简化项目结构，提高可维护性
- ✅ 支持独立的前端开发和部署
- ✅ 保持后端 API 的稳定性

## 🚀 使用方法

### 独立启动前端
```bash
# 从根目录启动
./start_frontend_only.sh

# 或进入前端目录启动
cd frontend
./start.sh
```

### 独立启动后端
```bash
python start_server.py
```

### 全栈启动
```bash
python start_all.py
```

## 🔧 开发建议

1. **前端开发**
   - 在 `frontend/` 目录下进行所有前端开发
   - 使用 `npm run dev` 启动开发服务器
   - 前端应用完全独立，可以单独部署

2. **后端开发**
   - 在根目录下进行 Python 后端开发
   - 使用 `python start_server.py` 启动后端服务
   - API 接口保持稳定，支持前端调用

3. **项目维护**
   - 前端和后端可以独立维护和更新
   - 通过 API 接口进行通信
   - 支持不同的部署策略

## 📝 注意事项

1. **路径引用**
   - 前端代码中的路径引用已经更新
   - 确保在正确的目录下运行命令

2. **依赖管理**
   - 前端依赖在 `frontend/` 目录下管理
   - 后端依赖在根目录下管理
   - 两个环境完全独立

3. **启动顺序**
   - 前端可以独立启动，但需要后端 API 支持
   - 建议先启动后端，再启动前端
   - 或使用 `start_all.py` 一键启动全栈
