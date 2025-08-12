#!/usr/bin/env python3
"""
Intent Router - 基于关键词/正则 + BM25稀疏检索的快速基线路由系统
"""

import re
import json
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import jieba
from rank_bm25 import BM25Okapi

class IntentRouter:
    """意图识别路由系统"""
    
    def __init__(self):
        # 意图模板和关键词
        self.intent_patterns = {
            "diet": {
                "keywords": ["减肥", "减重", "瘦身", "饮食", "营养", "食物", "吃饭", "餐", "卡路里", "热量"],
                "regex_patterns": [r"减肥|减重|瘦身", r"饮食|营养|食物", r"卡路里|热量"]
            },
            "exercise": {
                "keywords": ["运动", "健身", "锻炼", "跑步", "游泳", "骑行", "瑜伽", "力量训练", "有氧"],
                "regex_patterns": [r"运动|健身|锻炼", r"跑步|游泳|骑行", r"力量训练|有氧"]
            },
            "mental_health": {
                "keywords": ["心理", "情绪", "压力", "焦虑", "抑郁", "失眠", "睡眠", "放松", "冥想"],
                "regex_patterns": [r"心理|情绪|压力", r"焦虑|抑郁", r"失眠|睡眠"]
            },
            "general_wellness": {
                "keywords": ["健康", "养生", "保健", "预防", "体检", "医生", "医院", "症状", "疾病"],
                "regex_patterns": [r"健康|养生|保健", r"预防|体检", r"症状|疾病"]
            }
        }
        
        # 初始化BM25
        self.bm25 = None
        self.intent_docs = []
        self.intent_labels = []
        self._build_bm25_index()
        
        # 意图优先级权重
        self.intent_weights = {
            "diet": 1.0,
            "exercise": 1.0,
            "mental_health": 1.2,
            "general_wellness": 0.8
        }
    
    def _build_bm25_index(self):
        """构建BM25索引"""
        for intent, patterns in self.intent_patterns.items():
            keywords_text = " ".join(patterns["keywords"])
            regex_text = " ".join(patterns["regex_patterns"])
            
            self.intent_docs.extend([keywords_text, regex_text])
            self.intent_labels.extend([intent, intent])
        
        # 分词处理
        tokenized_docs = []
        for doc in self.intent_docs:
            tokens = list(jieba.cut(doc))
            tokenized_docs.append(tokens)
        
        # 构建BM25索引
        self.bm25 = BM25Okapi(tokenized_docs)
    
    def _keyword_match(self, text: str) -> Dict[str, float]:
        """关键词匹配"""
        scores = defaultdict(float)
        text_lower = text.lower()
        
        for intent, patterns in self.intent_patterns.items():
            score = 0.0
            for keyword in patterns["keywords"]:
                if keyword in text_lower:
                    score += 1.0
            scores[intent] = score
        
        return dict(scores)
    
    def _regex_match(self, text: str) -> Dict[str, float]:
        """正则表达式匹配"""
        scores = defaultdict(float)
        
        for intent, patterns in self.intent_patterns.items():
            score = 0.0
            for pattern in patterns["regex_patterns"]:
                matches = re.findall(pattern, text, re.IGNORECASE)
                score += len(matches)
            scores[intent] = score
        
        return dict(scores)
    
    def _bm25_match(self, text: str) -> Dict[str, float]:
        """BM25稀疏检索匹配"""
        if not self.bm25:
            return {}
        
        tokens = list(jieba.cut(text))
        bm25_scores = self.bm25.get_scores(tokens)
        
        intent_scores = defaultdict(float)
        for i, score in enumerate(bm25_scores):
            intent = self.intent_labels[i]
            intent_scores[intent] += score
        
        return dict(intent_scores)
    
    def route_intent(self, text: str) -> Tuple[str, float, Dict[str, float]]:
        """路由意图识别"""
        # 1. 关键词匹配
        keyword_scores = self._keyword_match(text)
        
        # 2. 正则表达式匹配
        regex_scores = self._regex_match(text)
        
        # 3. BM25稀疏检索匹配
        bm25_scores = self._bm25_match(text)
        
        # 4. 综合评分
        combined_scores = defaultdict(float)
        
        weights = {"keyword": 0.4, "regex": 0.3, "bm25": 0.3}
        
        for intent in self.intent_patterns.keys():
            combined_scores[intent] = (
                keyword_scores.get(intent, 0) * weights["keyword"] +
                regex_scores.get(intent, 0) * weights["regex"] +
                bm25_scores.get(intent, 0) * weights["bm25"]
            ) * self.intent_weights.get(intent, 1.0)
        
        # 5. 选择最佳意图
        if not combined_scores:
            return "general_wellness", 0.1, dict(combined_scores)
        
        best_intent = max(combined_scores.items(), key=lambda x: x[1])
        
        # 6. 计算置信度
        total_score = sum(combined_scores.values())
        confidence = best_intent[1] / total_score if total_score > 0 else 0.1
        
        return best_intent[0], confidence, dict(combined_scores)

# 意图映射到中文描述
INTENT_DESCRIPTIONS = {
    "diet": "饮食营养",
    "exercise": "运动健身", 
    "mental_health": "心理健康",
    "general_wellness": "一般健康"
}

def analyze_intent_advanced(user_input: str) -> Dict:
    """高级意图分析函数"""
    router = IntentRouter()
    
    # 路由意图
    primary_intent, confidence, all_scores = router.route_intent(user_input)
    
    # 构建结果
    result = {
        "primary_intent": primary_intent,
        "intent_description": INTENT_DESCRIPTIONS.get(primary_intent, "未知"),
        "confidence": confidence,
        "all_scores": all_scores,
        "user_input": user_input,
        "analysis_method": "keyword_regex_bm25_hybrid"
    }
    
    return result

# 测试函数
def test_intent_router():
    """测试意图路由器"""
    test_cases = [
        "我想减肥，有什么建议吗？",
        "我需要运动指导，包括适合我的运动类型",
        "我最近感觉很焦虑，睡眠质量不好",
        "我想了解如何改善整体健康状况"
    ]
    
    router = IntentRouter()
    
    print("🧪 意图路由器测试")
    print("=" * 50)
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n📝 测试 {i}: {text}")
        
        primary_intent, confidence, all_scores = router.route_intent(text)
        
        print(f"   🎯 主要意图: {primary_intent}")
        print(f"   📊 置信度: {confidence:.3f}")
        print(f"   📈 所有分数: {dict(all_scores)}")

if __name__ == "__main__":
    test_intent_router()
