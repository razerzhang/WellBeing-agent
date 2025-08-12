#!/usr/bin/env python3
"""
Intent Analysis Node - 使用新的意图路由器
"""

from typing import Dict, Any, Annotated
from langchain_core.messages import HumanMessage
from intent_router import analyze_intent_advanced

def analyze_intent_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    使用新的意图路由器分析用户意图
    
    Args:
        state: 当前状态
        
    Returns:
        更新后的状态
    """
    # 获取用户消息
    messages = state.get("messages", [])
    if not messages:
        return state
    
    # 获取最后一条用户消息
    last_message = messages[-1]
    if isinstance(last_message, HumanMessage):
        user_input = last_message.content
    else:
        user_input = str(last_message)
    
    # 使用新的意图路由器分析
    intent_result = analyze_intent_advanced(user_input)
    
    # 更新状态
    state.update({
        "current_step": "analyze_intent",
        "user_intent": intent_result["primary_intent"],
        "intent_confidence": intent_result["confidence"],
        "intent_scores": intent_result["all_scores"],
        "intent_description": intent_result["intent_description"],
        "analysis_method": intent_result["analysis_method"]
    })
    
    # 根据意图确定建议类型
    intent_mapping = {
        "diet": "diet",
        "exercise": "exercise", 
        "mental_health": "mental_health",
        "general_wellness": "general"
    }
    
    advice_type = intent_mapping.get(intent_result["primary_intent"], "general")
    state["advice_type"] = advice_type
    
    print(f"🎯 意图分析结果:")
    print(f"   主要意图: {intent_result['primary_intent']} ({intent_result['intent_description']})")
    print(f"   置信度: {intent_result['confidence']:.3f}")
    print(f"   建议类型: {advice_type}")
    print(f"   分析方法: {intent_result['analysis_method']}")
    
    return state

def analyze_intent_node_stream(state: Dict[str, Any]):
    """
    流式意图分析节点（用于兼容性）
    """
    # 直接调用非流式版本
    updated_state = analyze_intent_node(state)
    
    # 返回流式格式
    yield {
        'type': 'step',
        'step': 'analyze_intent',
        'message': f'📊 意图分析完成！检测到您需要 {updated_state.get("intent_description", "general")} 方面的建议',
        'intent': updated_state.get("user_intent"),
        'confidence': updated_state.get("intent_confidence")
    }
