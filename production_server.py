"""
FastAPI Server for 维尔必应 - Production Version
"""
import os
import sys

# Set LangSmith environment variables BEFORE importing anything else
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_TRACING"] = "true"

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Set API key if available
api_key = os.getenv("LANGCHAIN_API_KEY")
if api_key:
    os.environ["LANGCHAIN_API_KEY"] = api_key
    os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "wellbeing-agent")
    os.environ["LANGCHAIN_TAGS"] = "wellbeing-agent,production-server"
    print("🔗 LangSmith tracing enabled in production server")
    print(f"📊 Project: {os.environ['LANGCHAIN_PROJECT']}")
    print(f"🌐 Dashboard: https://smith.langchain.com/")
    print("✅ LangSmith environment variables set")
else:
    print("ℹ️  LangSmith tracing disabled - set LANGCHAIN_API_KEY to enable")

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
import asyncio
from typing import AsyncGenerator
import json

# Import the 维尔必应 agent AFTER setting environment variables
from wellbeing_agent import run_wellbeing_agent, run_wellbeing_agent_stream

app = FastAPI(
    title="维尔必应 API",
    description="健康顾问AI API服务",
    version="1.0.0"
)

# CORS配置 - 生产环境
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件（前端构建文件）
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")

# 数据模型
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/")
async def read_root():
    """根路径，返回前端页面"""
    return FileResponse("frontend/dist/index.html")

@app.get("/api/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "message": "维尔必应 API 运行正常"}

@app.post("/api/chat/stream")
async def chat_stream(message: ChatMessage):
    """流式聊天端点，处理用户消息通过维尔必应 agent"""
    async def generate_stream():
        try:
            # 发送开始信号
            start_data = {"type": "start", "message": "🌱 开始分析您的健康需求..."}
            yield f"data: {json.dumps(start_data, ensure_ascii=False)}\n\n"
            
            # 使用真正的流式函数
            async for chunk in run_wellbeing_agent_stream(message.message):
                if chunk['type'] == 'step':
                    # 步骤更新
                    yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
                elif chunk['type'] == 'content':
                    # 内容更新 - 逐字符流式输出
                    content = chunk.get('content', '')
                    if content:
                        # 模拟逐字符输出效果
                        for char in content:
                            char_data = {
                                "type": "content",
                                "content": char,
                                "advice_type": chunk.get('advice_type', 'general'),
                                "user_intent": chunk.get('user_intent', 'wellness')
                            }
                            yield f"data: {json.dumps(char_data, ensure_ascii=False)}\n\n"
                            await asyncio.sleep(0.02)  # 控制流式速度
                elif chunk['type'] == 'follow_up':
                    # 后续问题
                    yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
                elif chunk['type'] == 'summary':
                    # 总结
                    yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
                elif chunk['type'] == 'error':
                    # 错误处理
                    yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
                    break
            
            # 发送结束信号
            end_data = {"type": "end", "content": ""}
            yield f"data: {json.dumps(end_data, ensure_ascii=False)}\n\n"
            
        except Exception as e:
            error_data = {"type": "error", "message": f"服务器错误: {str(e)}"}
            yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/plain",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )

@app.post("/api/chat")
async def chat(message: ChatMessage):
    """普通聊天端点"""
    try:
        result = await run_wellbeing_agent(message.message)
        return ChatResponse(response=result.get("advice_result", "抱歉，我无法处理您的请求。"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")

if __name__ == "__main__":
    # 生产环境配置
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        "production_server:app",
        host=host,
        port=port,
        reload=False,  # 生产环境关闭热重载
        workers=1,     # 单进程，避免多进程LangSmith问题
        log_level="info"
    )
