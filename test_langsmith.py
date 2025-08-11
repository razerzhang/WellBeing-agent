#!/usr/bin/env python3
"""
LangSmith Integration Test
Tests the LangSmith integration with the Wellbeing Agent
"""

import os
import asyncio
from dotenv import load_dotenv
from langsmith import Client
from wellbeing_agent import run_wellbeing_agent

# Load environment variables
load_dotenv()

def test_langsmith_connection():
    """Test LangSmith API connection"""
    api_key = os.getenv("LANGCHAIN_API_KEY")
    if not api_key:
        print("❌ LANGCHAIN_API_KEY not found in environment variables")
        return False
    
    try:
        client = Client(api_key=api_key)
        # Test connection by getting projects
        projects = list(client.list_projects())
        print(f"✅ LangSmith connection successful")
        print(f"📊 Found {len(projects)} projects")
        return True
    except Exception as e:
        print(f"❌ LangSmith connection failed: {e}")
        return False

async def test_agent_tracing():
    """Test agent execution with LangSmith tracing"""
    print("\n🧪 Testing agent execution with LangSmith tracing...")
    
    test_inputs = [
        "我想减肥，有什么建议吗？",
        "我最近感觉很累，需要运动建议",
        "帮我制定一个健康的饮食计划"
    ]
    
    for i, user_input in enumerate(test_inputs, 1):
        print(f"\n📝 Test {i}: {user_input}")
        try:
            result = await run_wellbeing_agent(user_input)
            print(f"✅ Test {i} completed successfully")
            print(f"📄 Response: {result.get('advice_result', 'No advice generated')[:100]}...")
        except Exception as e:
            print(f"❌ Test {i} failed: {e}")

def check_environment():
    """Check environment configuration"""
    print("🔍 Checking environment configuration...")
    
    required_vars = [
        "LANGCHAIN_API_KEY",
        "LANGCHAIN_PROJECT", 
        "LANGCHAIN_TRACING_V2"
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value[:20]}{'...' if len(value) > 20 else ''}")
        else:
            print(f"❌ {var}: Not set")
    
    # Check LLM API keys
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if deepseek_key and deepseek_key.strip():
        print("✅ DEEPSEEK_API_KEY: Set")
    elif openai_key and openai_key.strip():
        print("✅ OPENAI_API_KEY: Set")
    else:
        print("❌ No LLM API key found (DEEPSEEK_API_KEY or OPENAI_API_KEY)")

async def main():
    """Main test function"""
    print("🔗 LangSmith Integration Test")
    print("=" * 40)
    
    # Check environment
    check_environment()
    
    # Test LangSmith connection
    if not test_langsmith_connection():
        print("\n❌ LangSmith connection failed. Please check your API key.")
        return
    
    # Test agent tracing
    await test_agent_tracing()
    
    print("\n🎉 Test completed!")
    print("\n📊 View traces in LangSmith:")
    print("   https://smith.langchain.com/")
    print(f"   Project: {os.getenv('LANGCHAIN_PROJECT', 'wellbeing-agent')}")

if __name__ == "__main__":
    asyncio.run(main())
