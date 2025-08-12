#!/usr/bin/env python3
"""
Wellbeing Agent - Health and Wellness Advisor
Provides personalized diet and exercise advice based on user intent.
"""

import os
import json
import asyncio
from typing import Dict, List, Any, TypedDict, Annotated, Optional, AsyncGenerator
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END, START

# Import DeepSeek LLM
from deepseek_llm import create_deepseek_llm, create_fallback_llm

# Load environment variables
load_dotenv()

# LangSmith Configuration
# According to https://docs.smith.langchain.com/, LangSmith tracing is automatically enabled
# when LANGCHAIN_API_KEY and LANGCHAIN_PROJECT are set
if os.getenv("LANGCHAIN_API_KEY"):
    print("🔗 LangSmith tracing enabled")
    print(f"📊 Project: {os.getenv('LANGCHAIN_PROJECT', 'wellbeing-agent')}")
    print(f"🌐 Dashboard: https://smith.langchain.com/")
    
    # Set additional LangSmith configuration for better tracing
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    
    # Optional: Set tags for better organization
    os.environ["LANGCHAIN_TAGS"] = "wellbeing-agent,health-advisor"
else:
    print("ℹ️  LangSmith tracing disabled - set LANGCHAIN_API_KEY to enable")

# Define the state structure
class WellbeingState(TypedDict):
    messages: Annotated[List, "The messages in the conversation"]
    current_step: Annotated[str, "The current step in the workflow"]
    user_intent: Annotated[Optional[str], "User's health and wellness intent"]
    advice_type: Annotated[Optional[str], "Type of advice: diet, exercise, or both"]
    user_profile: Annotated[Optional[Dict], "User's health profile and preferences"]
    advice_result: Annotated[Optional[str], "Generated health advice"]
    follow_up_questions: Annotated[Optional[List], "Follow-up questions for better advice"]
    
# Initialize the LLM
try:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if api_key and api_key.strip():
        llm = create_deepseek_llm()
        print("🤖 Using DeepSeek LLM")
    else:
        raise ValueError("DEEPSEEK_API_KEY is empty or not set")
except Exception as e:
    print(f"⚠️  DeepSeek LLM initialization failed: {e}")
    print("🔄 Falling back to OpenAI LLM...")
    llm = create_fallback_llm()
    if llm:
        print("✅ OpenAI fallback LLM initialized")
    else:
        print("❌ No LLM available. Please check your API keys.")
        print("   Set either DEEPSEEK_API_KEY or OPENAI_API_KEY in .env file")
        raise Exception("No LLM available. Please check your API keys.")

# Health and wellness knowledge base
class WellnessKnowledge:
    @staticmethod
    def get_diet_guidelines() -> Dict[str, Any]:
        """Get general diet guidelines."""
        return {
            "balanced_meal": {
                "protein": "Lean meats, fish, eggs, legumes, nuts",
                "carbohydrates": "Whole grains, fruits, vegetables",
                "fats": "Healthy fats from avocados, olive oil, nuts",
                "vitamins": "Colorful fruits and vegetables",
                "hydration": "8-10 glasses of water daily"
            },
            "meal_timing": {
                "breakfast": "Within 1 hour of waking",
                "lunch": "Midday, balanced with protein and carbs",
                "dinner": "2-3 hours before bedtime",
                "snacks": "Healthy options between meals"
            }
        }
    
    @staticmethod
    def get_exercise_guidelines() -> Dict[str, Any]:
        """Get general exercise guidelines."""
        return {
            "cardio": {
                "frequency": "3-5 times per week",
                "duration": "20-60 minutes",
                "intensity": "Moderate to vigorous",
                "examples": "Walking, running, cycling, swimming"
            },
            "strength": {
                "frequency": "2-3 times per week",
                "sets": "2-3 sets per exercise",
                "reps": "8-12 repetitions",
                "examples": "Bodyweight exercises, weight training"
            },
            "flexibility": {
                "frequency": "2-3 times per week",
                "duration": "10-15 minutes",
                "examples": "Stretching, yoga, tai chi"
            }
        }
    
    @staticmethod
    def get_health_tips() -> Dict[str, List[str]]:
        """Get general health tips."""
        return {
            "sleep": [
                "Aim for 7-9 hours of quality sleep",
                "Maintain consistent sleep schedule",
                "Create a relaxing bedtime routine"
            ],
            "stress_management": [
                "Practice deep breathing exercises",
                "Engage in regular physical activity",
                "Maintain social connections",
                "Consider meditation or mindfulness"
            ],
            "lifestyle": [
                "Limit processed foods and added sugars",
                "Avoid smoking and excessive alcohol",
                "Regular health check-ups",
                "Stay active throughout the day"
            ]
        }

def start_node(state: WellbeingState) -> WellbeingState:
    """Initialize the wellbeing agent state."""
    print("🌱 Wellbeing Agent starting...")
    return {
        **state,
        "current_step": "analyze_intent"
    }

def analyze_intent_node(state: WellbeingState) -> WellbeingState:
    """Analyze user's health and wellness intent."""
    messages = state["messages"]
    
    if not messages or not isinstance(messages[-1], HumanMessage):
        return {
            **state,
            "current_step": "end",
            "advice_result": "No user message found"
        }
    
    # Analyze user intent
    intent_prompt = SystemMessage(content="""
    You are a health and wellness expert. Analyze the user's message to understand their health intent.
    
    Determine:
    1. What type of advice they need (diet, exercise, general wellness, or specific health concern)
    2. Their current health status or goals
    3. Any specific preferences or restrictions
    
    Respond with JSON format:
    {
        "intent": "diet" | "exercise" | "wellness" | "specific_concern",
        "advice_type": "diet" | "exercise" | "both" | "general",
        "user_profile": {
            "goals": "string describing health goals",
            "preferences": "dietary or exercise preferences",
            "restrictions": "any health restrictions or limitations",
            "current_activity": "current exercise or diet habits"
        },
        "confidence": 0.0-1.0
    }
    """)
    
    try:
        analysis = llm.invoke([intent_prompt, messages[-1]])
        
        try:
            analysis_result = json.loads(analysis.content)
        except json.JSONDecodeError:
            analysis_result = {
                "intent": "wellness",
                "advice_type": "general",
                "user_profile": {
                    "goals": "general health improvement",
                    "preferences": "none specified",
                    "restrictions": "none specified",
                    "current_activity": "not specified"
                },
                "confidence": 0.5
            }
        
        return {
            **state,
            "current_step": "generate_advice",
            "user_intent": analysis_result.get("intent"),
            "advice_type": analysis_result.get("advice_type"),
            "user_profile": analysis_result.get("user_profile", {})
        }
    except Exception as error:
        print(f"Error in intent analysis: {error}")
        return {
            **state,
            "current_step": "generate_advice",
            "user_intent": "wellness",
            "advice_type": "general",
            "user_profile": {}
        }

def generate_advice_node(state: WellbeingState) -> WellbeingState:
    """Generate personalized health and wellness advice."""
    user_intent = state.get("user_intent", "wellness")
    advice_type = state.get("advice_type", "general")
    user_profile = state.get("user_profile", {})
    messages = state["messages"]
    
    # Get relevant knowledge
    knowledge = WellnessKnowledge()
    
    if advice_type == "diet" or advice_type == "both":
        diet_info = knowledge.get_diet_guidelines()
    else:
        diet_info = {}
    
    if advice_type == "exercise" or advice_type == "both":
        exercise_info = knowledge.get_exercise_guidelines()
    else:
        exercise_info = {}
    
    health_tips = knowledge.get_health_tips()
    
    # Generate personalized advice
    advice_prompt = SystemMessage(content=f"""
    You are a certified health and wellness coach. Generate personalized, actionable advice based on the user's intent.
    
    User Intent: {user_intent}
    Advice Type: {advice_type}
    User Profile: {json.dumps(user_profile, indent=2)}
    
    Available Knowledge:
    Diet Guidelines: {json.dumps(diet_info, indent=2) if diet_info else "Not applicable"}
    Exercise Guidelines: {json.dumps(exercise_info, indent=2) if exercise_info else "Not applicable"}
    Health Tips: {json.dumps(health_tips, indent=2)}
    
    Provide:
    1. Specific, actionable recommendations
    2. Evidence-based advice
    3. Practical tips that fit their lifestyle
    4. Safety considerations if applicable
    5. 2-3 follow-up questions to better understand their needs
    
    Format your response as a helpful, encouraging health coach would.
    """)
    
    try:
        advice_response = llm.invoke([advice_prompt, messages[-1]])
        
        # Extract follow-up questions
        follow_up_prompt = SystemMessage(content="""
        Based on the advice given, generate 2-3 follow-up questions to better understand the user's needs and provide more personalized recommendations.
        
        Questions should be:
        - Specific and actionable
        - Related to their health goals
        - Helpful for future advice customization
        
        Return as a JSON array of questions.
        """)
        
        follow_up_response = llm.invoke([follow_up_prompt, advice_response])
        
        try:
            follow_up_questions = json.loads(follow_up_response.content)
        except json.JSONDecodeError:
            follow_up_questions = [
                "How did you find implementing these recommendations?",
                "What specific challenges are you facing with your health goals?",
                "Would you like more detailed guidance on any particular aspect?"
            ]
        
        return {
            **state,
            "current_step": "end",
            "advice_result": advice_response.content,
            "follow_up_questions": follow_up_questions
        }
    except Exception as error:
        return {
            **state,
            "current_step": "end",
            "advice_result": f"Error generating advice: {str(error)}",
            "follow_up_questions": []
        }

async def generate_advice_node_stream(state: WellbeingState) -> AsyncGenerator[Dict[str, Any], None]:
    """Generate personalized health and wellness advice with streaming output."""
    user_intent = state.get("user_intent", "wellness")
    advice_type = state.get("advice_type", "general")
    user_profile = state.get("user_profile", {})
    messages = state["messages"]
    
    # Get relevant knowledge
    knowledge = WellnessKnowledge()
    
    if advice_type == "diet" or advice_type == "both":
        diet_info = knowledge.get_diet_guidelines()
    else:
        diet_info = {}
    
    if advice_type == "exercise" or advice_type == "both":
        exercise_info = knowledge.get_exercise_guidelines()
    else:
        exercise_info = {}
    
    health_tips = knowledge.get_health_tips()
    
    # Generate personalized advice with streaming
    advice_prompt = SystemMessage(content=f"""
    You are a certified health and wellness coach. Generate personalized, actionable advice based on the user's intent.
    
    User Intent: {user_intent}
    Advice Type: {advice_type}
    User Profile: {json.dumps(user_profile, indent=2)}
    
    Available Knowledge:
    Diet Guidelines: {json.dumps(diet_info, indent=2) if diet_info else "Not applicable"}
    Exercise Guidelines: {json.dumps(exercise_info, indent=2) if exercise_info else "Not applicable"}
    Health Tips: {json.dumps(health_tips, indent=2)}
    
    Provide:
    1. Specific, actionable recommendations
    2. Evidence-based advice
    3. Practical tips that fit their lifestyle
    4. Safety considerations if applicable
    5. 2-3 follow-up questions to better understand their needs
    
    Format your response as a helpful, encouraging health coach would.
    """)
    
    try:
        # Use streaming LLM call
        full_response = ""
        async for chunk in llm.ainvoke_stream([advice_prompt, messages[-1]]):
            full_response += chunk
            yield {
                'type': 'content',
                'content': chunk,
                'advice_type': advice_type,
                'user_intent': user_intent
            }
        
        # Generate follow-up questions
        follow_up_prompt = SystemMessage(content="""
        Based on the advice given, generate 2-3 follow-up questions to better understand the user's needs and provide more personalized recommendations.
        
        Questions should be:
        - Specific and actionable
        - Related to their health goals
        - Helpful for future advice customization
        
        Return as a JSON array of questions.
        """)
        
        follow_up_response = llm.invoke([follow_up_prompt, AIMessage(content=full_response)])
        
        try:
            follow_up_questions = json.loads(follow_up_response.content)
        except json.JSONDecodeError:
            follow_up_questions = [
                "How did you find implementing these recommendations?",
                "What specific challenges are you facing with your health goals?",
                "Would you like more detailed guidance on any particular aspect?"
            ]
        
        # Send follow-up questions
        yield {
            'type': 'follow_up',
            'questions': follow_up_questions,
            'message': '🤔 为了更好地帮助您，请考虑以下问题：'
        }
        
        # Update state
        state.update({
            "current_step": "end",
            "advice_result": full_response,
            "follow_up_questions": follow_up_questions
        })
        
    except Exception as error:
        yield {
            'type': 'error',
            'message': f'生成建议时出现错误: {str(error)}'
        }
        state.update({
            "current_step": "end",
            "advice_result": f"Error generating advice: {str(error)}",
            "follow_up_questions": []
        })

def end_node(state: WellbeingState) -> WellbeingState:
    """Finalize the wellbeing agent processing."""
    print("✅ Wellbeing Agent finished processing")
    
    advice_type = state.get("advice_type", "general")
    if advice_type == "diet":
        print("🥗 Provided dietary advice")
    elif advice_type == "exercise":
        print("🏃 Provided exercise advice")
    elif advice_type == "both":
        print("🥗🏃 Provided comprehensive diet and exercise advice")
    else:
        print("🌱 Provided general wellness advice")
    
    return state

# Create the graph
workflow = StateGraph(WellbeingState)

# Add nodes with descriptive names for LangSmith tracing
workflow.add_node("wellbeing_start", start_node)
workflow.add_node("wellbeing_analyze_intent", analyze_intent_node)
workflow.add_node("wellbeing_generate_advice", generate_advice_node)
workflow.add_node("wellbeing_end", end_node)

# Add edges
workflow.add_edge(START, "wellbeing_start")
workflow.add_edge("wellbeing_start", "wellbeing_analyze_intent")
workflow.add_edge("wellbeing_analyze_intent", "wellbeing_generate_advice")
workflow.add_edge("wellbeing_generate_advice", "wellbeing_end")
workflow.add_edge("wellbeing_end", END)

# Compile the graph
app = workflow.compile()

async def run_wellbeing_agent(user_input: str) -> Dict[str, Any]:
    """Run the wellbeing agent with user input."""
    print(f"\n👤 User: {user_input}")
    
    result = await app.ainvoke({
        "messages": [HumanMessage(content=user_input)]
    })
    
    print(f"\n🌱 Wellbeing Agent Advice:")
    print("=" * 50)
    print(result['advice_result'])
    
    if result.get('follow_up_questions'):
        print("\n🤔 Follow-up Questions:")
        for i, question in enumerate(result['follow_up_questions'], 1):
            print(f"{i}. {question}")
    
    return result

async def run_wellbeing_agent_stream(user_input: str):
    """Run the wellbeing agent with streaming output."""
    print(f"\n👤 User: {user_input}")

    # Initialize state with the user message
    state: WellbeingState = {
        "messages": [HumanMessage(content=user_input)]
    }

    # Execute start node to set initial state
    state = start_node(state)
    yield {
        'type': 'step',
        'step': 'start',
        'message': '🌱 开始分析您的健康需求...'
    }

    # Analyze user intent to determine advice type
    state = analyze_intent_node(state)
    yield {
        'type': 'step',
        'step': 'analyze_intent',
        'message': f'📊 分析完成！检测到您需要 {state.get("advice_type", "general")} 方面的建议'
    }

    # Generate advice with streaming output
    async for message_chunk in generate_advice_node_stream(state):
        if message_chunk['type'] == 'content':
            yield message_chunk
            await asyncio.sleep(0.05)  # Small delay for streaming effect
        elif message_chunk['type'] == 'follow_up':
            yield message_chunk
            break  # Stop streaming after follow-up questions
        elif message_chunk['type'] == 'error':
            yield message_chunk
            break  # Stop streaming on error

    # Final summary
    yield {
        'type': 'summary',
        'advice_type': state.get("advice_type", "general"),
        'message': f'✅ {state.get("advice_type", "general")} 建议生成完成！'
    }

async def interactive_mode():
    """Run the wellbeing agent in interactive mode."""
    print("🌱 Wellbeing Agent - Your Personal Health & Wellness Coach!")
    print("=" * 60)
    print("I can help you with:")
    print("🥗 Diet and nutrition advice")
    print("🏃 Exercise and fitness recommendations")
    print("🌱 General wellness tips")
    print("💪 Specific health concerns")
    print("\nType 'quit' to exit\n")
    
    while True:
        try:
            user_input = input("👤 You: ").strip()
            
            if user_input.lower() == 'quit':
                print("👋 Stay healthy and take care!")
                break
            
            if user_input:
                await run_wellbeing_agent(user_input)
                print("\n" + "=" * 50 + "\n")
            else:
                print("Please share your health and wellness question.")
                
        except KeyboardInterrupt:
            print("\n👋 Stay healthy and take care!")
            break
        except Exception as error:
            print(f"❌ Error: {error}")

async def main():
    """Main function."""
    import sys
    
    if len(sys.argv) > 1:
        # Command line mode
        user_input = " ".join(sys.argv[1:])
        await run_wellbeing_agent(user_input)
    else:
        # Interactive mode
        await interactive_mode()

if __name__ == "__main__":
    asyncio.run(main())
