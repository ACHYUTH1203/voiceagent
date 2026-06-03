import json
from typing import Literal

from state import AgentState
from llm import generate_llm_response


QualificationStage = Literal[
    "industry",
    "crm",
    "call_volume",
    "pain_points",
    "completed"
]


LEAD_QUALIFICATION_SYSTEM_PROMPT = """
You are Ezora's lead qualification analyst.

Your responsibilities:

1. Understand customer business context.
2. Extract lead information.
3. Maintain structured lead records.
4. Never hallucinate information.
5. Only extract information explicitly stated by the customer.
6. Preserve existing information if not updated.
7. Return ONLY valid JSON.

Fields:

industry
crm
call_volume
pain_points

Allowed industry values:

- real_estate
- healthcare
- ecommerce
- education
- service_business
- other
- unknown

Output Format:

{
    "industry": null,
    "crm": null,
    "call_volume": null,
    "pain_points": null
}
"""


LEAD_EXTRACTION_PROMPT = """
{system_prompt}

Current Lead Data:

{lead_data}

Conversation History:

{history}

Latest User Message:

{message}
"""
def calculate_lead_score(
    lead_data: dict
) -> int:

    score = 0

    if lead_data.get("industry"):
        score += 25

    if lead_data.get("crm"):
        score += 25

    if lead_data.get("call_volume"):
        score += 25

    if lead_data.get("pain_points"):
        score += 25

    return score
def determine_qualification_stage(
    lead_data: dict
) -> QualificationStage:

    if not lead_data.get("industry"):
        return "industry"

    if not lead_data.get("crm"):
        return "crm"

    if not lead_data.get("call_volume"):
        return "call_volume"

    if not lead_data.get("pain_points"):
        return "pain_points"

    return "completed"

def merge_lead_data(
    existing: dict,
    extracted: dict
) -> dict:

    merged = existing.copy()

    for key, value in extracted.items():

        if value is not None:

            merged[key] = value

    return merged

def lead_qualification_node(
    state: AgentState
) -> AgentState:


    if state.get("qualification_stage") == "completed" and not state.get("need_qualification"):
        return state

    history = state["messages"][-10:]

    prompt = LEAD_EXTRACTION_PROMPT.format(
        system_prompt=LEAD_QUALIFICATION_SYSTEM_PROMPT,
        lead_data=state["lead_data"],
        history=history,
        message=state["user_message"]
    )

    response = generate_llm_response(
        prompt
    )

    try:

        extracted_data = json.loads(
            response
        )

    except Exception:

        extracted_data = {}

    updated_lead_data = merge_lead_data(
        existing=state["lead_data"],
        extracted=extracted_data
    )

    lead_score = calculate_lead_score(
        updated_lead_data
    )

    qualification_stage = (
        determine_qualification_stage(
            updated_lead_data
        )
    )

    return {
        **state,

        "lead_data": updated_lead_data,

        "lead_score": lead_score,
        "qualification_stage": "industry", 
        "rewritten_query": "",

        "qualification_stage": qualification_stage
    }