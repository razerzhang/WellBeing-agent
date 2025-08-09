# 🚀 前端快速启动指南

## 立即开始

### 方法 1: 使用启动脚本（推荐）

```bash
./start_frontend.sh
```

### 方法 2: 手动启动

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 🌐 访问应用

应用启动后，在浏览器中打开：
**http://localhost:3000**

## ✨ 主要功能

### 🎯 快速咨询
- **饮食建议** 🥗 - 个性化营养搭配
- **运动指导** 🏃 - 科学运动计划
- **健康管理** 🌿 - 全方位健康指导
- **睡眠改善** 🌙 - 优质睡眠方案

### 🎨 界面特色
- 健康运动主题设计
- 流畅的动画效果
- 响应式布局设计
- 支持深色/浅色模式

### 🚀 流式输出
- 实时打字效果
- 可配置输出速度
- 美观的加载指示器

## 🛠️ 开发命令

```bash
# 开发模式
npm run dev

# 构建生产版本
npm run build

# 预览生产版本
npm run preview

# 代码检查
npm run lint
```

## 📱 响应式支持

- **桌面端**: 完整功能体验
- **平板端**: 触摸优化设计
- **移动端**: 移动优先布局

## 🔧 技术特性

- **React 18**: 最新 React 特性
- **TypeScript**: 类型安全开发
- **Tailwind CSS**: 实用优先样式
- **Framer Motion**: 流畅动画
- **Vite**: 快速构建工具

## 🎨 自定义主题

### 色彩系统
- Primary: 健康绿色
- Fitness: 运动橙色
- Wellness: 健康蓝色
- Energy: 活力黄色

### 组件样式
- 圆角设计语言
- 渐变色彩搭配
- 阴影层次效果
- 平滑过渡动画

## 📁 项目结构

```
src/
├── components/          # React 组件
│   ├── Sidebar.tsx     # 侧边栏
│   └── ChatInterface.tsx # 聊天界面
├── types.ts            # 类型定义
├── App.tsx             # 主应用
├── main.tsx            # 入口文件
└── index.css           # 全局样式
```

## 🚨 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 查找占用端口的进程
   lsof -i :3000
   
   # 终止进程
   kill -9 <PID>
   ```

2. **依赖安装失败**
   ```bash
   # 清除缓存
   npm cache clean --force
   
   # 重新安装
   rm -rf node_modules package-lock.json
   npm install
   ```

3. **构建失败**
   ```bash
   # 检查 TypeScript 错误
   npx tsc --noEmit
   
   # 检查 ESLint 错误
   npm run lint
   ```

### 环境要求

- **Node.js**: 16.0+
- **npm**: 8.0+
- **浏览器**: Chrome 90+, Firefox 88+, Safari 14+

## 🔮 下一步

1. 探索快速咨询功能
2. 体验流式输出效果
3. 尝试深色模式切换
4. 测试响应式布局

## 📞 支持

如果遇到问题：
1. 检查控制台错误信息
2. 查看网络请求状态
3. 确认依赖版本兼容性
4. 提交 Issue 或联系维护者

---

**享受你的健康之旅！** 🌱💪
