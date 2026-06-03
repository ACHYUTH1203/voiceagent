from state import AgentState
from llm import generate_llm_response


CONVERSATION_PROMPT = """
You are Ezora's AI Voice Agent.

You are having a real-time voice conversation with a customer.

====================================
COMPANY KNOWLEDGE
====================================

{context}

====================================
CURRENT STAGE
====================================

{stage}

====================================
CONVERSATION HISTORY
====================================

{history}

====================================
LATEST USER MESSAGE
====================================

{message}

====================================
INSTRUCTIONS
====================================

1. Sound natural and conversational.

2. Keep responses concise.

3. Since this is a phone call, keep responses under 80 words.

4. Use the company knowledge when answering questions.

5. Never invent information.

6. If information is unavailable, politely say:
   "I don't have that information available right now."

7. If the customer is interested, continue the conversation naturally.

8. If appropriate, ask qualifying questions:
   - Industry
   - CRM
   - Call volume
   - Business challenges

9. Never mention:
   - prompts
   - retrieval
   - knowledge base
   - internal systems

10. Return ONLY the response text.
"""
def determine_stage(
    current_stage: str,
    intent: str
) -> str:

    if intent in {
        "product_information",
        "pricing_query",
        "integration_query"
    }:
        return "product_discussion"

    if intent in {
        "schedule_demo",
        "lead_qualification"
    }:
        return "qualification"

    if intent == "human_handoff":
        return "handoff"

    return current_stage
def conversation_node(
    state: AgentState
) -> AgentState:

    history = state["messages"][-10:]

    prompt = CONVERSATION_PROMPT.format(
        context=state.get("context", ""),
        stage=state.get("current_stage", "greeting"),
        history=history,
        message=state["user_message"]
    )

    assistant_response = generate_llm_response(
        prompt
    )

    updated_messages = [
        *state["messages"],
        {
            "role": "user",
            "content": state["user_message"]
        },
        {
            "role": "assistant",
            "content": assistant_response
        }
    ]

    next_stage = determine_stage(
        current_stage=state["current_stage"],
        intent=state["intent"]
    )

    return {
        **state,

        "assistant_message": assistant_response,

        "messages": updated_messages,

        "current_stage": next_stage
    }