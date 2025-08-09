# Wellbeing Agent 前端应用

这是 Wellbeing Agent 的前端应用，使用 React + TypeScript + Tailwind CSS 构建。

## 🏗️ 项目结构

```
frontend/
├── src/                    # React 源代码
│   ├── components/         # React 组件
│   │   ├── ChatInterface.tsx
│   │   └── Sidebar.tsx
│   ├── App.tsx            # 主应用组件
│   ├── main.tsx           # 应用入口点
│   ├── types.ts           # TypeScript 类型定义
│   └── index.css          # 全局样式
├── index.html              # HTML 入口文件
├── package.json            # 项目依赖配置
├── tsconfig.json           # TypeScript 配置
├── vite.config.ts          # Vite 构建配置
├── tailwind.config.js      # Tailwind CSS 配置
├── postcss.config.js       # PostCSS 配置
└── start.sh               # 前端启动脚本
```

## 🚀 快速开始

### 安装依赖
```bash
cd frontend
npm install
```

### 启动开发服务器
```bash
# 方法1：使用启动脚本
./start.sh

# 方法2：直接使用 npm
npm run dev
```

### 构建生产版本
```bash
npm run build
```

### 预览生产版本
```bash
npm run preview
```

## 🛠️ 技术栈

- **React 18** - 用户界面库
- **TypeScript** - 类型安全的 JavaScript
- **Tailwind CSS** - 实用优先的 CSS 框架
- **Vite** - 快速的前端构建工具
- **Framer Motion** - 动画库
- **Lucide React** - 图标库

## 🎨 设计特色

- 健康运动主题色彩系统
- 响应式设计，支持移动端和桌面端
- 流畅的动画和交互效果
- 深色模式支持
- 流式输出支持

## 🔧 开发说明

### 组件结构
- `App.tsx` - 主应用容器
- `Sidebar.tsx` - 侧边栏导航组件
- `ChatInterface.tsx` - 聊天界面组件

### 样式系统
- 使用 Tailwind CSS 进行样式管理
- 自定义颜色主题和动画
- 响应式断点设计

### API 集成
- 通过 Vite 代理配置连接后端 API
- 支持流式响应处理
- 错误处理和状态管理

## 📱 浏览器支持

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🚀 部署

前端应用可以部署到任何静态文件托管服务：

- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront

构建后的文件位于 `dist/` 目录。
