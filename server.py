#!/usr/bin/env python3
"""
FastAPI Server for Wellbeing Agent
Provides HTTP API endpoints for the frontend to communicate with the LangGraph agent.
"""

import os
import asyncio
import json
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Import the wellbeing agent
from wellbeing_agent import run_wellbeing_agent, run_wellbeing_agent_stream

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Wellbeing Agent API",
    description="Health and wellness advice API powered by LangGraph",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    follow_up_questions: list = []
    advice_type: str = "general"
    user_intent: str = "wellness"

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Wellbeing Agent API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint that processes user messages through the wellbeing agent."""
    try:
        print(f"📨 Received message: {request.message}")
        
        # Process the message through the wellbeing agent
        result = await run_wellbeing_agent(request.message)
        
        # Extract the response data
        response_data = {
            "response": result.get("advice_result", "Sorry, I couldn't generate advice at the moment."),
            "follow_up_questions": result.get("follow_up_questions", []),
            "advice_type": result.get("advice_type", "general"),
            "user_intent": result.get("user_intent", "wellness")
        }
        
        print(f"✅ Generated response for: {request.message[:50]}...")
        return ChatResponse(**response_data)
        
    except Exception as e:
        print(f"❌ Error processing message: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing message: {str(e)}"
        )

@app.post("/api/chat/stream")
async def stream_chat_endpoint(request: ChatRequest):
    """Streamed chat endpoint that processes user messages through the wellbeing agent."""
    async def generate_stream():
        try:
            print(f"📨 Received streaming message: {request.message}")
            
            # Create a message placeholder first
            yield f"data: {json.dumps({'type': 'start', 'message': '开始生成建议...'})}\n\n"
            
            # Process the message through the wellbeing agent with streaming
            async for chunk in run_wellbeing_agent_stream(request.message):
                if chunk:
                    yield f"data: {json.dumps(chunk)}\n\n"
            
            # Send end signal
            yield f"data: {json.dumps({'type': 'end', 'message': '建议生成完成'})}\n\n"
            
        except Exception as e:
            print(f"❌ Error in streaming: {e}")
            error_data = {
                'type': 'error',
                'message': f'处理消息时出现错误: {str(e)}'
            }
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )

@app.get("/api/quick-actions")
async def get_quick_actions():
    """Get available quick action suggestions."""
    return {
        "actions": [
            {
                "id": "diet",
                "title": "饮食建议",
                "description": "获取个性化的饮食和营养建议",
                "icon": "🥗"
            },
            {
                "id": "exercise", 
                "title": "运动指导",
                "description": "专业的运动计划和健身指导",
                "icon": "🏃"
            },
            {
                "id": "wellness",
                "title": "健康生活",
                "description": "全面的健康生活方式建议",
                "icon": "🌱"
            },
            {
                "id": "sleep",
                "title": "睡眠改善",
                "description": "改善睡眠质量的实用建议",
                "icon": "😴"
            },
            {
                "id": "mental",
                "title": "心理健康",
                "description": "压力管理和心理健康支持",
                "icon": "🧠"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment or use default
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Starting Wellbeing Agent API server on port {port}")
    print(f"📱 Frontend should connect to: http://localhost:{port}")
    print(f"🔗 API documentation: http://localhost:{port}/docs")
    
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
