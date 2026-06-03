import json
from typing import Literal

from state import AgentState
from llm import generate_llm_response


Sentiment = Literal[
    "positive",
    "neutral",
    "negative"
]


CallOutcome = Literal[
    "qualified_lead",
    "unqualified_lead",
    "follow_up_required",
    "demo_requested",
    "support_request",
    "human_handoff",
    "not_interested",
    "unknown"
]
ANALYTICS_SYSTEM_PROMPT = """
You are Ezora's call analytics engine.

Your responsibility is to analyze the call and generate structured analytics.

Analyze:

1. Overall customer sentiment
2. Call outcome

Sentiment Options:

- positive
- neutral
- negative

Call Outcome Options:

- qualified_lead
- unqualified_lead
- follow_up_required
- demo_requested
- support_request
- human_handoff
- not_interested
- unknown

Rules:

1. Use the entire conversation.
2. Use lead qualification information if available.
3. Never hallucinate.
4. Return ONLY valid JSON.

Output Format:

{
    "sentiment": "positive",
    "call_outcome": "qualified_lead"
}
"""
ANALYTICS_PROMPT = """
{system_prompt}

Conversation History:

{history}

Detected Intent:

{intent}

Lead Data:

{lead_data}

Lead Score:

{lead_score}
"""



def analytics_node(
    state: AgentState
) -> AgentState:


    if not state.get("call_completed"):
        return {
            **state,
            "sentiment": None,
            "call_outcome": None
        }

    history = state["messages"][-20:]

    prompt = ANALYTICS_PROMPT.format(
        system_prompt=ANALYTICS_SYSTEM_PROMPT,
        history=history,
        intent=state["intent"],
        lead_data=state["lead_data"],
        lead_score=state["lead_score"]
    )

    response = generate_llm_response(
        prompt
    )

    try:

        analytics = json.loads(
            response
        )

    except Exception:

        analytics = {
            "sentiment": "neutral",
            "call_outcome": "unknown"
        }

    sentiment = analytics.get(
        "sentiment",
        "neutral"
    )

    call_outcome = analytics.get(
        "call_outcome",
        "unknown"
    )

    return {
        **state,

        "sentiment": sentiment,

        "call_outcome": call_outcome
    }