from typing import TypedDict, List, Dict, Optional


class AgentState(TypedDict):

    # Call Information
    call_id: str
    session_id: str
    phone_number: str

    # Current Turn
    user_message: str
    assistant_message: str

    # Conversation History
    messages: List[Dict]

    # Intent
    intent: Optional[str]
    intent_confidence: float

    # RAG
    retrieved_docs: List[Dict]
    context: str

    # Routing
    requires_rag: bool
    requires_human: bool
    need_qualification: bool
    need_end_call: bool

    # Lead Qualification
    lead_data: Dict
    lead_score: int

    # Analytics
    sentiment: Optional[str]
    call_outcome: Optional[str]

    # Conversation Stage
    current_stage: str

    # Metadata
    timestamp: str

    system_prompt: str

    qualification_stage: str
    rewritten_query: str
    call_completed: bool