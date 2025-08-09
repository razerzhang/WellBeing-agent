#!/usr/bin/env python3
"""
Setup script for LangGraph Agent project
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create .env file if it doesn't exist."""
    env_path = Path(".env")
    if not env_path.exists():
        print("📝 Creating .env file...")
        
        env_content = """# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Optional: OpenAI Organization ID
OPENAI_ORG_ID=your_organization_id_here
"""
        
        with open(env_path, 'w') as f:
            f.write(env_content)
        
        print("✅ .env file created successfully!")
        print("⚠️  Please edit .env file and add your OpenAI API key")
    else:
        print("✅ .env file already exists")

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        'langgraph',
        'langchain',
        'langchain-openai',
        'python-dotenv',
        'pydantic'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("📦 Missing dependencies detected:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nPlease run: pip install -r requirements.txt")
    else:
        print("✅ All dependencies are installed")

def main():
    """Main setup function."""
    print("🚀 LangGraph Agent Setup")
    print("=" * 40)
    
    # Create .env file
    create_env_file()
    
    # Check dependencies
    check_dependencies()
    
    print("\n🎯 Next steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Run 'pip install -r requirements.txt' to install dependencies")
    print("3. Run 'python main.py' to start the basic agent")
    print("4. Run 'python advanced_agent.py' to test the advanced agent")
    print("5. Run 'python test_agent.py' to run the test suite")
    
    print("\n📚 Available commands:")
    print("- python main.py                    : Start basic agent (interactive)")
    print("- python main.py \"your message\"     : Run basic agent with message")
    print("- python advanced_agent.py          : Run advanced agent (interactive)")
    print("- python advanced_agent.py \"message\" : Run advanced agent with message")
    print("- python test_agent.py              : Run test suite")
    
    print("\n✨ Setup complete! Happy coding!")

if __name__ == "__main__":
    main()
