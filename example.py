#!/usr/bin/env python3
"""
Example usage of LangGraph Agent
"""

import asyncio
from main import run_agent
from advanced_agent import run_advanced_agent

async def basic_example():
    """Example of using the basic agent."""
    print("=== Basic Agent Example ===")
    
    # Example 1: Simple conversation
    await run_agent("Hello, how are you?")
    
    # Example 2: Question about AI
    await run_agent("What is artificial intelligence?")

async def advanced_example():
    """Example of using the advanced agent."""
    print("\n=== Advanced Agent Example ===")
    
    # Example 1: Mathematical calculation
    await run_advanced_agent("What is 15 * 23?")
    
    # Example 2: Weather information
    await run_advanced_agent("What's the weather like in Beijing?")
    
    # Example 3: Complex calculation
    await run_advanced_agent("Calculate (25 + 17) * 3 / 2")
    
    # Example 4: Weather for unknown city
    await run_advanced_agent("What's the weather in Tokyo?")

async def main():
    """Run all examples."""
    print("🚀 LangGraph Agent Examples")
    print("=" * 40)
    
    # Run basic agent examples
    await basic_example()
    
    # Run advanced agent examples
    await advanced_example()
    
    print("\n✨ Examples completed!")

if __name__ == "__main__":
    asyncio.run(main())
