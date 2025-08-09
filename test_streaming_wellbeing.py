#!/usr/bin/env python3
"""
Test script for Wellbeing Agent streaming output
"""

import asyncio
import sys
import os

# Add current directory to path to import wellbeing_agent
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from wellbeing_agent import run_wellbeing_agent_stream

async def test_streaming():
    """Test the streaming functionality of the wellbeing agent."""
    
    # Test cases
    test_cases = [
        "我想减肥，请给我一些饮食建议",
        "我需要一个健身计划来增肌",
        "最近工作压力很大，有什么健康建议吗？",
        "我想改善睡眠质量"
    ]
    
    print("🧪 测试 Wellbeing Agent 流式输出功能")
    print("=" * 60)
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n📝 测试用例 {i}: {test_input}")
        print("-" * 50)
        
        try:
            async for chunk in run_wellbeing_agent_stream(test_input):
                if chunk['type'] == 'step':
                    print(f"🔄 {chunk['message']}")
                elif chunk['type'] == 'content':
                    print(chunk['content'], end='', flush=True)
                elif chunk['type'] == 'follow_up':
                    print(f"\n\n🤔 {chunk['message']}")
                    for j, question in enumerate(chunk['questions'], 1):
                        print(f"   {j}. {question}")
                elif chunk['type'] == 'summary':
                    print(f"\n\n✅ {chunk['message']}")
                elif chunk['type'] == 'error':
                    print(f"\n❌ {chunk['message']}")
                
                # Small delay to see streaming effect
                await asyncio.sleep(0.1)
            
            print("\n" + "=" * 60)
            
        except Exception as e:
            print(f"❌ 测试用例 {i} 失败: {e}")
            print("=" * 60)

async def test_single_streaming():
    """Test a single streaming interaction."""
    
    print("🧪 测试单个流式交互")
    print("=" * 60)
    
    user_input = "我想学习如何做健康的早餐"
    print(f"👤 用户输入: {user_input}")
    print("-" * 50)
    
    try:
        async for chunk in run_wellbeing_agent_stream(user_input):
            if chunk['type'] == 'step':
                print(f"🔄 {chunk['message']}")
            elif chunk['type'] == 'content':
                print(chunk['content'], end='', flush=True)
            elif chunk['type'] == 'follow_up':
                print(f"\n\n🤔 {chunk['message']}")
                for i, question in enumerate(chunk['questions'], 1):
                    print(f"   {i}. {question}")
            elif chunk['type'] == 'summary':
                print(f"\n\n✅ {chunk['message']}")
            elif chunk['type'] == 'error':
                print(f"\n❌ {chunk['message']}")
            
            # Small delay to see streaming effect
            await asyncio.sleep(0.05)
            
    except Exception as e:
        print(f"❌ 流式输出测试失败: {e}")

async def main():
    """Main function."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "single":
            await test_single_streaming()
        else:
            print("用法: python test_streaming_wellbeing.py [single]")
            print("  single: 测试单个流式交互")
            print("  无参数: 运行所有测试用例")
    else:
        await test_streaming()

if __name__ == "__main__":
    asyncio.run(main())
