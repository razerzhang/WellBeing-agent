# LangSmith 集成指南

本文档介绍如何为维尔必应健康顾问AI应用集成LangSmith，实现可视化追踪链路。

## 什么是LangSmith？

[LangSmith](https://docs.smith.langchain.com/) 是一个用于构建生产级LLM应用的平台，提供：

- **Observability（可观测性）**: 分析追踪链路，配置指标、仪表板和告警
- **Evaluation（评估）**: 评估应用性能，获取人工反馈
- **Prompt Engineering（提示工程）**: 迭代优化提示，自动版本控制

## 快速开始

### 1. 获取LangSmith API密钥

1. 访问 [LangSmith](https://smith.langchain.com/)
2. 注册账户并登录
3. 在设置中获取API密钥

### 2. 配置环境变量

复制 `env.example` 到 `.env` 并配置：

```bash
# LangSmith Configuration
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=wellbeing-agent
LANGCHAIN_TRACING_V2=true
```

### 3. 启动应用

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动后端服务
python production_server.py

# 启动前端服务
cd frontend && npm run dev
```

## 追踪链路可视化

### 在LangSmith中查看

1. 访问 [LangSmith Dashboard](https://smith.langchain.com/)
2. 选择 `wellbeing-agent` 项目
3. 查看实时追踪链路

### 追踪链路结构

应用的工作流包含以下节点：

```
START
  ↓
wellbeing_start (初始化状态)
  ↓
wellbeing_analyze_intent (分析用户意图)
  ↓
wellbeing_generate_advice (生成健康建议)
  ↓
wellbeing_end (完成处理)
  ↓
END
```

### 每个节点的功能

1. **wellbeing_start**: 初始化工作流状态
2. **wellbeing_analyze_intent**: 分析用户健康需求意图
3. **wellbeing_generate_advice**: 生成个性化健康建议
4. **wellbeing_end**: 整理输出结果

## 监控指标

LangSmith提供以下关键指标：

- **请求响应时间**: 每个节点的执行时间
- **错误率**: 失败请求的统计
- **成本分析**: API调用成本追踪
- **用户交互**: 用户输入和AI响应的质量

## 调试和优化

### 查看详细追踪

1. 在LangSmith中选择任意追踪链路
2. 查看每个节点的输入输出
3. 分析LLM调用的详细信息

### 性能优化

1. 识别耗时最长的节点
2. 优化提示词和模型参数
3. 监控成本和使用量

### 错误排查

1. 查看错误追踪链路
2. 分析失败原因
3. 优化错误处理逻辑

## 高级功能

### 自定义评估

```python
# 在wellbeing_agent.py中添加评估逻辑
from langsmith import Client

client = Client()
# 创建评估数据集和指标
```

### 提示词版本管理

1. 在LangSmith中创建提示词
2. 版本控制和A/B测试
3. 性能对比分析

### 生产监控

1. 设置告警规则
2. 监控关键指标
3. 实时问题检测

## 故障排除

### 常见问题

1. **API密钥无效**
   - 检查LANGCHAIN_API_KEY是否正确
   - 确认账户权限

2. **追踪不显示**
   - 确认LANGCHAIN_TRACING_V2=true
   - 检查网络连接

3. **项目不存在**
   - 确认LANGCHAIN_PROJECT设置
   - 在LangSmith中创建项目

### 调试命令

```bash
# 检查环境变量
echo $LANGCHAIN_API_KEY
echo $LANGCHAIN_PROJECT

# 测试连接
curl -H "Authorization: Bearer $LANGCHAIN_API_KEY" \
     https://api.smith.langchain.com/runs
```

## 最佳实践

1. **项目命名**: 使用描述性的项目名称
2. **节点命名**: 为每个节点使用清晰的名称
3. **错误处理**: 完善错误追踪和日志
4. **性能监控**: 定期检查关键指标
5. **成本控制**: 监控API使用成本

## 更多资源

- [LangSmith官方文档](https://docs.smith.langchain.com/)
- [LangGraph集成指南](https://docs.smith.langchain.com/docs/langgraph)
- [API参考](https://api.smith.langchain.com/)
- [社区支持](https://github.com/langchain-ai/langsmith)
