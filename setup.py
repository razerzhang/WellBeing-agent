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
        
        # Copy from env.example
        example_path = Path("env.example")
        if example_path.exists():
            with open(example_path, 'r') as f:
                env_content = f.read()
        else:
            env_content = """# DeepSeek API Configuration
DEEPSEEK_API_KEY=
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1

# Optional: Model Configuration
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_TEMPERATURE=0.0

# OpenAI API Key (fallback)
OPENAI_API_KEY=your_openai_api_key_here
"""
        
        with open(env_path, 'w') as f:
            f.write(env_content)
        
        print("✅ .env file created successfully!")
        print("⚠️  Please edit .env file and add your API keys")
    else:
        print("✅ .env file already exists")

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        'langgraph',
        'langchain',
        'langchain-openai',
        'python-dotenv',
        'pydantic',
        'fastapi',
        'uvicorn'
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
    print("1. Edit .env file and add your API keys")
    print("2. Run 'pip install -r requirements.txt' to install dependencies")
    print("3. Run 'python production_server.py' to start the production server")
    print("4. Run 'cd frontend && npm install && npm run dev' to start the frontend")
    
    print("\n📚 Available commands:")
    print("- python production_server.py       : Start production server")
    print("- python wellbeing_agent.py         : Run wellbeing agent (interactive)")
    print("- python wellbeing_agent.py \"message\" : Run wellbeing agent with message")
    print("- cd frontend && npm run dev        : Start frontend development server")
    print("- cd frontend && npm run build      : Build frontend for production")
    
    print("\n✨ Setup complete! Happy coding!")

if __name__ == "__main__":
    main()
