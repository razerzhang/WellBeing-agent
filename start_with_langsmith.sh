#!/bin/bash

# Start Wellbeing Agent with LangSmith Monitoring
echo "🔗 Starting Wellbeing Agent with LangSmith Integration"
echo "====================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check LangSmith configuration
if [ -z "$LANGCHAIN_API_KEY" ]; then
    echo "⚠️  LANGCHAIN_API_KEY not set. Loading from .env file..."
    if [ -f ".env" ]; then
        export $(cat .env | grep -v '^#' | xargs)
    fi
fi

if [ -z "$LANGCHAIN_API_KEY" ]; then
    echo "❌ LangSmith API key not found. Please set LANGCHAIN_API_KEY in .env file"
    echo "   Run: ./setup_langsmith.sh for setup instructions"
    exit 1
fi

echo "✅ LangSmith configuration loaded"
echo "📊 Project: ${LANGCHAIN_PROJECT:-wellbeing-agent}"
echo "🌐 Dashboard: https://smith.langchain.com/"

# Function to show menu
show_menu() {
    echo ""
    echo "🔧 Available Commands:"
    echo "1. Test LangSmith Integration"
    echo "2. Run Agent in Interactive Mode"
    echo "3. Start Production Server"
    echo "4. Monitor LangSmith Traces"
    echo "5. View LangSmith Dashboard"
    echo "6. Exit"
    echo ""
    read -p "Choose an option (1-6): " choice
}

# Main loop
while true; do
    show_menu
    
    case $choice in
        1)
            echo "🧪 Testing LangSmith Integration..."
            python test_langsmith.py
            ;;
        2)
            echo "🌱 Starting Interactive Mode..."
            python wellbeing_agent.py
            ;;
        3)
            echo "🚀 Starting Production Server..."
            python production_server.py
            ;;
        4)
            echo "📊 Monitoring LangSmith Traces..."
            python langsmith_monitor.py
            ;;
        5)
            echo "🌐 Opening LangSmith Dashboard..."
            open "https://smith.langchain.com/"
            ;;
        6)
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo "❌ Invalid option. Please choose 1-6."
            ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
done
