#!/usr/bin/env python3
"""
Advanced LangGraph Agent - Python Version with DeepSeek
An advanced agent with tool usage capabilities.
"""

import os
import json
import asyncio
from typing import Dict, List, Any, TypedDict, Annotated, Optional
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END, START

# Import DeepSeek LLM
from deepseek_llm import create_deepseek_llm, create_fallback_llm

# Load environment variables
load_dotenv()

# Define the state structure
class AdvancedAgentState(TypedDict):
    messages: Annotated[List, "The messages in the conversation"]
    current_step: Annotated[str, "The current step in the workflow"]
    result: Annotated[str, "The result of the current step"]
    tools_used: Annotated[List, "List of tools used"]
    needs_tool: Annotated[bool, "Whether a tool is needed"]
    tool_name: Annotated[Optional[str], "Name of the tool to use"]
    tool_input: Annotated[Optional[str], "Input for the tool"]
    tool_result: Annotated[Optional[str], "Result from tool execution"]
    reasoning: Annotated[Optional[str], "Reasoning for tool usage"]

# Initialize the LLM
try:
    llm = create_deepseek_llm()
    print("🤖 Using DeepSeek LLM")
except Exception as e:
    print(f"⚠️  DeepSeek LLM initialization failed: {e}")
    print("🔄 Falling back to OpenAI LLM...")
    llm = create_fallback_llm()
    if llm:
        print("✅ OpenAI fallback LLM initialized")
    else:
        raise Exception("No LLM available. Please check your API keys.")

# Tool definitions
class Tools:
    @staticmethod
    def calculator(expression: str) -> str:
        """Perform mathematical calculations."""
        try:
            # Safe evaluation - only allow basic math operations
            import re
            sanitized = re.sub(r'[^0-9+\-*/().]', '', expression)
            result = eval(sanitized)
            return str(result)
        except Exception as error:
            return f"Error: {str(error)}"
    
    @staticmethod
    def weather(location: str) -> str:
        """Get weather information (mock)."""
        weather_data = {
            "beijing": "Sunny, 25°C",
            "shanghai": "Cloudy, 22°C",
            "guangzhou": "Rainy, 28°C",
            "default": "Partly cloudy, 20°C"
        }
        return weather_data.get(location.lower(), weather_data["default"])

def start_node(state: AdvancedAgentState) -> AdvancedAgentState:
    """Initialize the agent state."""
    print("🤖 Advanced Agent starting...")
    return {
        **state,
        "current_step": "analyze"
    }

def analyze_node(state: AdvancedAgentState) -> AdvancedAgentState:
    """Analyze if the message needs tools."""
    messages = state["messages"]
    
    if not messages or not isinstance(messages[-1], HumanMessage):
        return {
            **state,
            "current_step": "end",
            "result": "No user message found"
        }
    
    # Analyze if the message needs tools
    analysis_prompt = SystemMessage(content="""
    Analyze the user's message and determine if any tools are needed.
    Available tools:
    - calculator: for mathematical calculations
    - weather: for weather information
    
    Respond with JSON format:
    {
        "needs_tool": true/false,
        "tool_name": "calculator" or "weather" or null,
        "tool_input": "the input for the tool" or null,
        "reasoning": "explanation of your decision"
    }
    """)
    
    try:
        analysis = llm.invoke([analysis_prompt, messages[-1]])
        
        try:
            analysis_result = json.loads(analysis.content)
        except json.JSONDecodeError:
            analysis_result = {
                "needs_tool": False,
                "tool_name": None,
                "tool_input": None,
                "reasoning": "Failed to parse analysis"
            }
        
        return {
            **state,
            "current_step": "use_tool" if analysis_result.get("needs_tool") else "respond",
            "needs_tool": analysis_result.get("needs_tool", False),
            "tool_name": analysis_result.get("tool_name"),
            "tool_input": analysis_result.get("tool_input"),
            "reasoning": analysis_result.get("reasoning")
        }
    except Exception as error:
        print(f"Error in analysis: {error}")
        return {
            **state,
            "current_step": "respond",
            "needs_tool": False
        }

def use_tool_node(state: AdvancedAgentState) -> AdvancedAgentState:
    """Execute the required tool."""
    tool_name = state.get("tool_name")
    tool_input = state.get("tool_input")
    tools_used = state.get("tools_used", [])
    
    if not tool_name or not tool_input:
        return {
            **state,
            "current_step": "respond",
            "result": "Tool information missing"
        }
    
    try:
        if tool_name == "calculator":
            tool_result = Tools.calculator(tool_input)
        elif tool_name == "weather":
            tool_result = Tools.weather(tool_input)
        else:
            return {
                **state,
                "current_step": "respond",
                "result": f"Tool {tool_name} not found"
            }
        
        tool_usage = {
            "tool": tool_name,
            "input": tool_input,
            "output": tool_result,
            "timestamp": str(asyncio.get_event_loop().time())
        }
        
        return {
            **state,
            "tools_used": tools_used + [tool_usage],
            "current_step": "respond",
            "tool_result": tool_result
        }
    except Exception as error:
        return {
            **state,
            "current_step": "respond",
            "result": f"Tool execution failed: {str(error)}"
        }

def respond_node(state: AdvancedAgentState) -> AdvancedAgentState:
    """Generate the final response."""
    messages = state["messages"]
    tool_result = state.get("tool_result")
    reasoning = state.get("reasoning")
    
    context = ""
    if tool_result:
        context += f"\nTool result: {tool_result}"
    if reasoning:
        context += f"\nReasoning: {reasoning}"
    
    response_prompt = SystemMessage(content=f"""
    You are a helpful AI assistant. {context}
    Provide a clear and helpful response to the user's message.
    """)
    
    try:
        response = llm.invoke([response_prompt, messages[-1]])
        
        return {
            **state,
            "messages": messages + [response],
            "current_step": "end",
            "result": response.content
        }
    except Exception as error:
        return {
            **state,
            "current_step": "end",
            "result": f"Error generating response: {str(error)}"
        }

def end_node(state: AdvancedAgentState) -> AdvancedAgentState:
    """Finalize the agent processing."""
    print("✅ Advanced Agent finished processing")
    tools_used = state.get("tools_used", [])
    if tools_used:
        tool_names = [f"{t['tool']}({t['input']})" for t in tools_used]
        print(f"🔧 Tools used: {', '.join(tool_names)}")
    return state

# Create the graph
workflow = StateGraph(AdvancedAgentState)

# Add nodes
workflow.add_node("start", start_node)
workflow.add_node("analyze", analyze_node)
workflow.add_node("use_tool", use_tool_node)
workflow.add_node("respond", respond_node)
workflow.add_node("end", end_node)

# Add edges
workflow.add_edge(START, "start")
workflow.add_edge("start", "analyze")
workflow.add_conditional_edges(
    "analyze",
    lambda state: "use_tool" if state.get("needs_tool") else "respond"
)
workflow.add_edge("use_tool", "respond")
workflow.add_edge("respond", "end") 
workflow.add_edge("end", END)

# Compile the graph
app = workflow.compile()

async def run_advanced_agent(user_input: str) -> Dict[str, Any]:
    """Run the advanced agent with user input."""
    print(f"\n👤 User: {user_input}")
    
    result = await app.ainvoke({
        "messages": [HumanMessage(content=user_input)]
    })
    
    print(f"🤖 Advanced Agent: {result['result']}")
    return result

async def interactive_mode():
    """Run the advanced agent in interactive mode."""
    print("🚀 Advanced LangGraph Agent started!")
    print("Type 'quit' to exit\n")
    
    while True:
        try:
            user_input = input("👤 You: ").strip()
            
            if user_input.lower() == 'quit':
                print("👋 Goodbye!")
                break
            
            if user_input:
                await run_advanced_agent(user_input)
            else:
                print("Please enter a message.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as error:
            print(f"❌ Error: {error}")

async def main():
    """Main function."""
    import sys
    
    if len(sys.argv) > 1:
        # Command line mode
        user_input = " ".join(sys.argv[1:])
        await run_advanced_agent(user_input)
    else:
        # Interactive mode
        await interactive_mode()

if __name__ == "__main__":
    asyncio.run(main())
