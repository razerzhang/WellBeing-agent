#!/usr/bin/env python3
"""
Test Production Server LangSmith Integration
"""

import requests
import json
import time
from datetime import datetime

def test_production_langsmith():
    """Test LangSmith integration with production server"""
    print("🧪 Testing Production Server LangSmith Integration")
    print("=" * 60)
    
    # Test health endpoint
    print("1. Testing health endpoint...")
    try:
        health_response = requests.get("http://localhost:8000/api/health")
        if health_response.status_code == 200:
            print("✅ Health endpoint working")
            print(f"   Response: {health_response.json()}")
        else:
            print(f"❌ Health endpoint failed: {health_response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("   Make sure production_server.py is running")
        return
    
    # Test chat endpoint
    print("\n2. Testing chat endpoint...")
    test_messages = [
        "我想减肥，有什么建议吗？",
        "我最近感觉很累，需要运动建议"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n   Test {i}: {message}")
        try:
            response = requests.post(
                "http://localhost:8000/api/chat",
                json={"message": message},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success")
                print(f"   Response: {result.get('response', '')[:100]}...")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test streaming endpoint
    print("\n3. Testing streaming endpoint...")
    try:
        response = requests.post(
            "http://localhost:8000/api/chat/stream",
            json={"message": "帮我制定一个健康的饮食计划"},
            stream=True,
            timeout=30
        )
        
        if response.status_code == 200:
            print("   ✅ Streaming endpoint working")
            print("   Receiving stream data...")
            
            # Read a few chunks to verify streaming
            chunk_count = 0
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    chunk_count += 1
                    if chunk_count <= 3:  # Only show first 3 chunks
                        print(f"   Chunk {chunk_count}: {chunk.decode('utf-8')[:100]}...")
                    elif chunk_count == 4:
                        print("   ... (more chunks)")
                        break
        else:
            print(f"   ❌ Streaming failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Streaming error: {e}")
    
    print("\n4. LangSmith Integration Check")
    print("   📊 Check LangSmith Dashboard: https://smith.langchain.com/")
    print("   🔍 Look for traces with tag: 'wellbeing-agent,production-server'")
    print("   ⏰ Wait a few minutes for traces to appear")
    
    print("\n🎉 Test completed!")
    print("   If you see traces in LangSmith, the integration is working correctly.")

if __name__ == "__main__":
    test_production_langsmith()
