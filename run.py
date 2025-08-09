#!/usr/bin/env python3
"""
Quick start script for LangGraph Agent
"""

import sys
import asyncio
from pathlib import Path

def check_env():
    """Check if .env file exists and has API key."""
    env_path = Path(".env")
    if not env_path.exists():
        print("⚠️  .env file not found!")
        print("Please run 'python setup.py' first to create it.")
        return False
    
    with open(env_path, 'r') as f:
        content = f.read()
        if 'your_openai_api_key_here' in content:
            print("⚠️  Please edit .env file and add your OpenAI API key!")
            return False
    
    return True

async def main():
    """Main function."""
    print("🚀 LangGraph Agent Quick Start")
    print("=" * 40)
    
    # Check environment
    if not check_env():
        sys.exit(1)
    
    print("\nChoose an option:")
    print("1. Basic Agent (interactive)")
    print("2. Advanced Agent (interactive)")
    print("3. Run examples")
    print("4. Run tests")
    print("5. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                print("\nStarting Basic Agent...")
                from main import interactive_mode
                await interactive_mode()
                break
            elif choice == '2':
                print("\nStarting Advanced Agent...")
                from advanced_agent import interactive_mode
                await interactive_mode()
                break
            elif choice == '3':
                print("\nRunning examples...")
                from example import main as run_examples
                await run_examples()
                break
            elif choice == '4':
                print("\nRunning tests...")
                from test_agent import run_tests
                await run_tests()
                break
            elif choice == '5':
                print("👋 Goodbye!")
                break
            else:
                print("Please enter a valid choice (1-5).")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as error:
            print(f"❌ Error: {error}")

if __name__ == "__main__":
    asyncio.run(main())
