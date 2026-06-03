import json

from state import AgentState
from llm import generate_llm_response


INTENT_PROMPT = """
You are an expert conversational AI system for an AI Voice Agent.

Your job is to:

1. Understand the full conversation.
2. Rewrite the user's latest message into a standalone query.
3. Classify the user's intent.
4. Return ONLY valid JSON.

------------------------------------
Conversation History:
{history}

Latest User Message:
{message}
------------------------------------

Intent Options:

- product_information
- pricing_query
- integration_query
- schedule_demo
- reschedule_demo
- support_request
- complaint
- lead_qualification
- human_handoff
- general_conversation

Instructions:

- Use conversation history to resolve references.
- Expand pronouns and implicit references.
- Rewrite the latest user message into a complete standalone query.
- Choose the single best intent.
- Confidence must be between 0 and 1.
- Return ONLY JSON.

Output Schema:

{{
    "rewritten_query": "...",
    "intent": "...",
    "confidence": 0.95
}}
"""

def intent_router_node(state: AgentState) -> AgentState:

    message = state["user_message"]
    history = state["messages"][-10:]
    response = generate_llm_response(
        INTENT_PROMPT.format(
            history=history,
            message=message
        )
    )
    

    

    result = json.loads(response)

    intent = result.get(
        "intent",
        "general_conversation"
    )

    confidence = result.get(
        "confidence",
        0.0
    )
    rewritten_query = result.get(
    "rewritten_query",
    message
    )

    requires_rag = intent in {
        "product_information",
        "pricing_query",
        "integration_query",
        "support_request",
    }

    need_qualification = intent in {
        "schedule_demo",
        "lead_qualification",
    }

    requires_human = (
        intent == "human_handoff"
    )

    need_end_call = any(
        phrase in message.lower()
        for phrase in [
            "bye",
            "goodbye",
            "not interested",
            "busy",
            "call later",
        ]
    )
    need_end_call = any(
        phrase in message.lower()
        for phrase in [
            "bye",
            "goodbye",
            "not interested",
            "busy",
            "call later",
        ]
    )

    return {
        **state,

        "intent": intent,
        "intent_confidence": confidence,
        "rewritten_query": rewritten_query,

        "requires_rag": requires_rag,
        "need_qualification": need_qualification,

        "requires_human": requires_human,
        "need_end_call": need_end_call,
        "call_completed": need_end_call,
    }