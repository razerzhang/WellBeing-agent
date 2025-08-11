#!/bin/bash

# LangSmith Setup Script
echo "🔗 LangSmith Setup for Wellbeing Agent"
echo "======================================"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "✅ .env file created"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "📋 Next steps to enable LangSmith:"
echo ""
echo "1. Get your LangSmith API key:"
echo "   - Visit: https://smith.langchain.com/"
echo "   - Sign up/Login to your account"
echo "   - Go to Settings > API Keys"
echo "   - Create a new API key"
echo ""
echo "2. Update your .env file:"
echo "   - Open .env file"
echo "   - Set LANGCHAIN_API_KEY=your_api_key_here"
echo "   - Save the file"
echo ""
echo "3. Test the integration:"
echo "   python test_langsmith.py"
echo ""
echo "4. View traces in LangSmith:"
echo "   https://smith.langchain.com/"
echo ""
echo "📚 For more details, see: LANGSMITH_SETUP.md"
