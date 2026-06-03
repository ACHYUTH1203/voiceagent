from uuid import uuid4
from datetime import datetime

from state import AgentState


def call_init_node(state: AgentState) -> AgentState:

    opening_message = (
        "Hi, this is the AI assistant from Ezora. "
        "We help businesses automate customer conversations using AI voice agents. "
        "Do you have a minute to chat?"
    )


    return {
        **state,

        "call_id": str(uuid4()),
        "session_id": str(uuid4()),

        "assistant_message": opening_message,

        "messages": [
            {
                "role": "assistant",
                "content": opening_message
            }
        ],

        "intent": None,
        "intent_confidence": 0.0,

        "retrieved_docs": [],
        "context": "",

        "requires_rag": False,
        "requires_human": False,
        "need_qualification": False,
        "need_end_call": False,

        
        "lead_data": {
        "industry": None,
        "crm": None,
        "call_volume": None,
        "pain_points": None
        },
        "lead_score": 0,

        "sentiment": None,
        "call_outcome": None,

        "current_stage": "greeting",

        "timestamp": datetime.utcnow().isoformat()
    }