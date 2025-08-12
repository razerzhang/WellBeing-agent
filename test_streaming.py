
#!/usr/bin/env python3
"""
Test Streaming Output
"""

import asyncio
from wellbeing_agent import run_wellbeing_agent_stream

async def test_streaming():
    """测试流式输出"""
    print("🧪 测试流式输出功能")
    print("=" * 50)
    
    test_input = "我想减肥，有什么建议吗？"
    print(f"📝 测试输入: {test_input}")
    print("\n🔄 开始流式输出:")
    print("-" * 30)
    
    content_buffer = ""
    
    async for chunk in run_wellbeing_agent_stream(test_input):
        if chunk['type'] == 'step':
            print(f"\n📊 {chunk['message']}")
        elif chunk['type'] == 'content':
            content_buffer += chunk['content']
            print(chunk['content'], end='', flush=True)
        elif chunk['type'] == 'follow_up':
            print(f"\n\n🤔 {chunk['message']}")
            for i, question in enumerate(chunk['questions'], 1):
                print(f"   {i}. {question}")
        elif chunk['type'] == 'summary':
            print(f"\n\n✅ {chunk['message']}")
        elif chunk['type'] == 'error':
            print(f"\n❌ {chunk['message']}")
    
    print(f"\n\n📄 完整内容长度: {len(content_buffer)} 字符")

if __name__ == "__main__":
    asyncio.run(test_streaming())
