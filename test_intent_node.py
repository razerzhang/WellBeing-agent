#!/usr/bin/env python3
"""
Test Intent Analysis Node
"""

import asyncio
from langchain_core.messages import HumanMessage
from intent_analysis_node import analyze_intent_node

def test_intent_analysis():
    """测试意图分析节点"""
    print("🧪 测试新的意图分析节点")
    print("=" * 50)
    
    test_cases = [
        "我想减肥，有什么建议吗？",
        "我需要运动指导，包括适合我的运动类型",
        "我最近感觉很焦虑，睡眠质量不好",
        "我想了解如何改善整体健康状况",
        "帮我制定一个健康的饮食计划",
        "我经常头痛，应该怎么办？",
        "我想练习瑜伽来放松身心",
        "如何提高我的免疫力？"
    ]
    
    for i, user_input in enumerate(test_cases, 1):
        print(f"\n📝 测试 {i}: {user_input}")
        
        # 创建初始状态
        state = {
            "messages": [HumanMessage(content=user_input)],
            "current_step": "start"
        }
        
        # 运行意图分析
        result = analyze_intent_node(state)
        
        print(f"   🎯 主要意图: {result.get('user_intent')}")
        print(f"   📊 置信度: {result.get('intent_confidence', 0):.3f}")
        print(f"   📋 描述: {result.get('intent_description')}")
        print(f"   🔧 建议类型: {result.get('advice_type')}")
        print(f"   🛠️  分析方法: {result.get('analysis_method')}")
        
        # 显示所有分数
        scores = result.get('intent_scores', {})
        if scores:
            print(f"   📈 所有分数:")
            for intent, score in scores.items():
                print(f"      {intent}: {score:.3f}")

if __name__ == "__main__":
    test_intent_analysis()
