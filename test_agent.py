#!/usr/bin/env python3
"""
Test suite for LangGraph Agent
"""

import asyncio
from advanced_agent import run_advanced_agent

# Test cases for the advanced agent
test_cases = [
    {
        "name": "Basic conversation",
        "input": "Hello, how are you?",
        "expected": "conversation"
    },
    {
        "name": "Mathematical calculation",
        "input": "What is 15 * 23?",
        "expected": "calculator"
    },
    {
        "name": "Weather information",
        "input": "What's the weather like in Beijing?",
        "expected": "weather"
    },
    {
        "name": "Complex calculation",
        "input": "Calculate (25 + 17) * 3 / 2",
        "expected": "calculator"
    },
    {
        "name": "Weather for unknown city",
        "input": "What's the weather in Tokyo?",
        "expected": "weather"
    }
]

async def run_tests():
    """Run the test suite."""
    print("🧪 Running LangGraph Agent Tests\n")
    
    for test_case in test_cases:
        print(f"\n📋 Test: {test_case['name']}")
        print(f"Input: \"{test_case['input']}\"")
        print("─" * 50)
        
        try:
            result = await run_advanced_agent(test_case['input'])
            print("✅ Test completed successfully")
            
            # Check if tools were used as expected
            tools_used = result.get('tools_used', [])
            
            if test_case['expected'] == 'calculator' and any(t['tool'] == 'calculator' for t in tools_used):
                print("✅ Calculator tool used as expected")
            elif test_case['expected'] == 'weather' and any(t['tool'] == 'weather' for t in tools_used):
                print("✅ Weather tool used as expected")
            elif test_case['expected'] == 'conversation' and not tools_used:
                print("✅ Conversation handled without tools as expected")
            else:
                print("⚠️  Tool usage pattern not as expected")
                
        except Exception as error:
            print(f"❌ Test failed: {error}")
        
        print("─" * 50)
    
    print("\n🎉 All tests completed!")

async def main():
    """Main function for running tests."""
    await run_tests()

if __name__ == "__main__":
    asyncio.run(main())
