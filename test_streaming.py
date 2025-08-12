import os
import asyncio
import pytest

# Ensure a dummy OpenAI key so module initialization succeeds
os.environ.setdefault("OPENAI_API_KEY", "test")
os.environ.setdefault("DEEPSEEK_API_KEY", "test")

import wellbeing_agent


def test_run_wellbeing_agent_stream(monkeypatch):
    def fake_start_node(state):
        state["current_step"] = "analyze_intent"
        return state

    def fake_analyze_intent_node(state):
        state.update({
            "user_intent": "wellness",
            "advice_type": "general",
            "current_step": "generate_advice",
        })
        return state

    async def fake_generate_advice_node_stream(state):
        yield {
            'type': 'content',
            'content': 'test advice',
            'advice_type': state['advice_type'],
            'user_intent': state['user_intent'],
        }
        yield {
            'type': 'follow_up',
            'questions': ['Q1'],
            'message': 'msg'
        }

    async def fake_ainvoke(*args, **kwargs):
        raise AssertionError("app.ainvoke should not be called")

    monkeypatch.setattr(wellbeing_agent, "start_node", fake_start_node)
    monkeypatch.setattr(wellbeing_agent, "analyze_intent_node", fake_analyze_intent_node)
    monkeypatch.setattr(wellbeing_agent, "generate_advice_node_stream", fake_generate_advice_node_stream)
    monkeypatch.setattr(wellbeing_agent.app, "ainvoke", fake_ainvoke)

    chunks = []

    async def collect():
        async for chunk in wellbeing_agent.run_wellbeing_agent_stream("hello"):
            chunks.append(chunk)

    asyncio.run(collect())

    assert [chunks[0]['step'], chunks[1]['step']] == ['start', 'analyze_intent']
    follow_up_index = next(i for i, c in enumerate(chunks) if c['type'] == 'follow_up')
    assert any(c['type'] == 'content' for c in chunks[2:follow_up_index])
    assert all(c['type'] != 'content' for c in chunks[follow_up_index+1:])
    assert chunks[-1]['type'] == 'summary'
