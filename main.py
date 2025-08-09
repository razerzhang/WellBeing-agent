#!/usr/bin/env python3
"""
LangGraph Agent - Python Version with DeepSeek
A simple agent using LangGraph for workflow management.
"""

import os
import asyncio
from typing import Dict, List, Any, TypedDict, Annotated
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END, START

# Import DeepSeek LLM
from deepseek_llm import create_deepseek_llm, create_fallback_llm

# Load environment variables
load_dotenv()

# Define the state structure
class AgentState(TypedDict):
    messages: Annotated[List, "The messages in the conversation"]
    current_step: Annotated[str, "The current step in the workflow"]
    result: Annotated[str, "The result of the current step"]

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

def start_node(state: AgentState) -> AgentState:
    """Initialize the agent state."""
    print("🤖 Agent starting...")
    return {
        **state,
        "current_step": "process"
    }

def process_node(state: AgentState) -> AgentState:
    """Process the user message with LLM."""
    messages = state["messages"]
    
    if not messages or not isinstance(messages[-1], HumanMessage):
        return {
            **state,
            "current_step": "end",
            "result": "No user message found"
        }
    
    try:
        # Process the message with LLM
        response = llm.invoke([messages[-1]])
        
        return {
            **state,
            "messages": messages + [response],
            "current_step": "end",
            "result": response.content
        }
    except Exception as error:
        print(f"Error processing message: {error}")
        return {
            **state,
            "current_step": "end",
            "result": f"Error: {str(error)}"
        }

def end_node(state: AgentState) -> AgentState:
    """Finalize the agent processing."""
    print("✅ Agent finished processing")
    return state

# Create the graph using the new API
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("start", start_node)
workflow.add_node("process", process_node)
workflow.add_node("end", end_node)

# Add edges
workflow.add_edge(START, "start")
workflow.add_edge("start", "process")
workflow.add_edge("process", "end")
workflow.add_edge("end", END)

# Compile the graph
app = workflow.compile()

async def run_agent(user_input: str) -> Dict[str, Any]:
    """Run the agent with user input."""
    print(f"\n👤 User: {user_input}")
    
    result = await app.ainvoke({
        "messages": [HumanMessage(content=user_input)]
    })
    
    print(f"🤖 Agent: {result['result']}")
    return result

async def interactive_mode():
    """Run the agent in interactive mode."""
    print("🚀 LangGraph Agent started!")
    print("Type 'quit' to exit\n")
    
    while True:
        try:
            user_input = input("👤 You: ").strip()
            
            if user_input.lower() == 'quit':
                print("👋 Goodbye!")
                break
            
            if user_input:
                await run_agent(user_input)
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
        await run_agent(user_input)
    else:
        # Interactive mode
        await interactive_mode()

if __name__ == "__main__":
    asyncio.run(main())
