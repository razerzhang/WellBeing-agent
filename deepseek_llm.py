#!/usr/bin/env python3
"""
DeepSeek LLM Integration for LangGraph Agent
"""

import os
import json
import requests
from typing import List, Dict, Any, Optional, AsyncGenerator, Generator
from langchain_core.language_models.llms import LLM
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.outputs import LLMResult, Generation

class DeepSeekLLM(LLM):
    """DeepSeek LLM wrapper for LangChain."""
    
    api_key: str
    base_url: str = "https://api.deepseek.com/v1"
    model: str = "deepseek-chat"
    temperature: float = 0.0
    max_tokens: int = 4096
    
    @property
    def _llm_type(self) -> str:
        return "deepseek"
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs) -> str:
        """Call the DeepSeek API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        if stop:
            data["stop"] = stop
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"DeepSeek API request failed: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Failed to parse DeepSeek API response: {str(e)}")
    
    def invoke(self, messages: List[BaseMessage], **kwargs) -> AIMessage:
        """Invoke the LLM with a list of messages."""
        # Convert messages to DeepSeek format
        deepseek_messages = []
        
        for message in messages:
            if isinstance(message, HumanMessage):
                deepseek_messages.append({
                    "role": "user",
                    "content": message.content
                })
            elif isinstance(message, AIMessage):
                deepseek_messages.append({
                    "role": "assistant",
                    "content": message.content
                })
            elif isinstance(message, SystemMessage):
                deepseek_messages.append({
                    "role": "system",
                    "content": message.content
                })
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": deepseek_messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            return AIMessage(content=content)
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"DeepSeek API request failed: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Failed to parse DeepSeek API response: {str(e)}")

    def invoke_stream(self, messages: List[BaseMessage], **kwargs) -> Generator[str, None, None]:
        """Stream invoke the DeepSeek API."""
        # Convert messages to DeepSeek format
        deepseek_messages = []
        
        for message in messages:
            if isinstance(message, HumanMessage):
                deepseek_messages.append({
                    "role": "user",
                    "content": message.content
                })
            elif isinstance(message, AIMessage):
                deepseek_messages.append({
                    "role": "assistant",
                    "content": message.content
                })
            elif isinstance(message, SystemMessage):
                deepseek_messages.append({
                    "role": "system",
                    "content": message.content
                })
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": deepseek_messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": True  # 启用流式输出
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                stream=True,  # requests 的流式参数
                timeout=30
            )
            response.raise_for_status()
            
            # 处理流式响应
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    
                    # 跳过 "data: [DONE]" 行
                    if line_str == "data: [DONE]":
                        break
                    
                    # 解析 SSE 格式的数据
                    if line_str.startswith("data: "):
                        try:
                            data_str = line_str[6:]  # 移除 "data: " 前缀
                            if data_str.strip():
                                chunk_data = json.loads(data_str)
                                
                                # 提取 delta content
                                if "choices" in chunk_data and len(chunk_data["choices"]) > 0:
                                    choice = chunk_data["choices"][0]
                                    if "delta" in choice and "content" in choice["delta"]:
                                        content = choice["delta"]["content"]
                                        if content:
                                            yield content
                                            
                        except json.JSONDecodeError:
                            # 忽略无效的 JSON 行
                            continue
                            
        except requests.exceptions.RequestException as e:
            raise Exception(f"DeepSeek API streaming request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to process streaming response: {str(e)}")

    async def ainvoke_stream(self, messages: List[BaseMessage], **kwargs) -> AsyncGenerator[str, None]:
        """Async stream invoke the DeepSeek API."""
        # 将同步流式调用包装为异步
        for chunk in self.invoke_stream(messages, **kwargs):
            yield chunk

def create_deepseek_llm() -> DeepSeekLLM:
    """Create a DeepSeek LLM instance with environment configuration."""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY environment variable is required")
    
    base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
    model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    temperature = float(os.getenv("DEEPSEEK_TEMPERATURE", "0.0"))
    
    return DeepSeekLLM(
        api_key=api_key,
        base_url=base_url,
        model=model,
        temperature=temperature
    )

def create_fallback_llm():
    """Create a fallback LLM (OpenAI) if DeepSeek is not available."""
    try:
        from langchain_openai import ChatOpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key != "your_openai_api_key_here":
            llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0,
                api_key=api_key
            )
            
            # Add ainvoke_stream method for compatibility
            async def ainvoke_stream(messages, **kwargs):
                """Async stream wrapper for ChatOpenAI."""
                try:
                    # Use astream for streaming
                    async for chunk in llm.astream(messages, **kwargs):
                        if hasattr(chunk, 'content') and chunk.content:
                            yield chunk.content
                except Exception as e:
                    # Fallback to non-streaming if streaming fails
                    response = await llm.ainvoke(messages, **kwargs)
                    if hasattr(response, 'content'):
                        yield response.content
            
            # Add the method to the LLM instance
            llm.ainvoke_stream = ainvoke_stream
            return llm
    except ImportError:
        pass
    
    return None
