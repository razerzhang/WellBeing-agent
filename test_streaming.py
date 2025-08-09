#!/usr/bin/env python3
"""
测试流式输出功能的脚本
"""

import asyncio
import aiohttp
import json
import time

async def test_streaming_api():
    """测试流式API端点"""
    print("🧪 开始测试流式输出功能...")
    print("=" * 50)
    
    # 测试消息
    test_messages = [
        "我想了解健康饮食的建议",
        "我需要运动指导，包括适合我的运动类型",
        "如何改善睡眠质量？",
        "我想了解如何管理压力"
    ]
    
    async with aiohttp.ClientSession() as session:
        for i, message in enumerate(test_messages, 1):
            print(f"\n📝 测试 {i}: {message}")
            print("-" * 40)
            
            try:
                # 发送流式请求
                async with session.post(
                    'http://localhost:8000/api/chat/stream',
                    json={'message': message},
                    headers={'Content-Type': 'application/json'}
                ) as response:
                    
                    if response.status == 200:
                        print("✅ 流式响应开始:")
                        
                        # 读取流式数据
                        async for line in response.content:
                            line = line.decode('utf-8').strip()
                            
                            if line.startswith('data: '):
                                try:
                                    data = json.loads(line[6:])
                                    print(f"📊 数据类型: {data.get('type', 'unknown')}")
                                    
                                    if data.get('type') == 'content':
                                        print(f"📝 内容: {data.get('content', '')}")
                                    elif data.get('type') == 'step':
                                        print(f"🔄 步骤: {data.get('message', '')}")
                                    elif data.get('type') == 'follow_up':
                                        print(f"🤔 跟进问题: {data.get('message', '')}")
                                        if data.get('questions'):
                                            for j, q in enumerate(data.get('questions', []), 1):
                                                print(f"   {j}. {q}")
                                    elif data.get('type') == 'summary':
                                        print(f"✅ 总结: {data.get('message', '')}")
                                    elif data.get('type') == 'error':
                                        print(f"❌ 错误: {data.get('message', '')}")
                                    else:
                                        print(f"📄 数据: {data}")
                                        
                                except json.JSONDecodeError as e:
                                    print(f"❌ JSON解析错误: {e}")
                                    print(f"原始数据: {line}")
                    else:
                        print(f"❌ HTTP错误: {response.status}")
                        error_text = await response.text()
                        print(f"错误详情: {error_text}")
                        
            except Exception as e:
                print(f"❌ 请求错误: {e}")
            
            # 等待一下再进行下一个测试
            await asyncio.sleep(2)
    
    print("\n" + "=" * 50)
    print("🎯 流式输出测试完成!")

async def test_regular_api():
    """测试普通API端点作为对比"""
    print("\n🧪 测试普通API端点作为对比...")
    print("=" * 50)
    
    test_message = "我想了解健康饮食的建议"
    print(f"📝 测试消息: {test_message}")
    
    async with aiohttp.ClientSession() as session:
        try:
            start_time = time.time()
            
            async with session.post(
                'http://localhost:8000/api/chat',
                json={'message': test_message},
                headers={'Content-Type': 'application/json'}
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    end_time = time.time()
                    
                    print(f"✅ 响应时间: {end_time - start_time:.2f}秒")
                    print(f"📝 响应内容: {data.get('response', '')[:200]}...")
                    print(f"🤔 跟进问题: {data.get('follow_up_questions', [])}")
                    print(f"🏷️ 建议类型: {data.get('advice_type', '')}")
                else:
                    print(f"❌ HTTP错误: {response.status}")
                    
        except Exception as e:
            print(f"❌ 请求错误: {e}")

async def test_api_health():
    """测试API健康状态"""
    print("\n🏥 测试API健康状态...")
    print("=" * 50)
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('http://localhost:8000/health') as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ API状态: {data}")
                else:
                    print(f"❌ API不健康: {response.status}")
        except Exception as e:
            print(f"❌ 无法连接到API: {e}")

async def main():
    """主函数"""
    print("🚀 Wellbeing Agent 流式输出测试")
    print("=" * 60)
    
    # 首先测试API健康状态
    await test_api_health()
    
    # 测试流式输出
    await test_streaming_api()
    
    # 测试普通API作为对比
    await test_regular_api()
    
    print("\n🎉 所有测试完成!")

if __name__ == "__main__":
    asyncio.run(main())
