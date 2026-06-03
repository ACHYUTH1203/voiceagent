# from langgraph.graph import StateGraph
# from langgraph.graph import START, END

# from state import AgentState

# from call_init_node import call_init_node
# from intent_router_node import intent_router_node
# from rag_node import rag_node
# from conversation_node import conversation_node
# from lead_qualification_node import (
#     lead_qualification_node
# )
# from analytics_node import analytics_node


# def route_after_intent(
#     state: AgentState
# ):

#     if state["requires_rag"]:
#         return "rag"

#     return "conversation"


# builder = StateGraph(AgentState)

# # Nodes
# builder.add_node(
#     "call_init",
#     call_init_node
# )

# builder.add_node(
#     "intent_router",
#     intent_router_node
# )

# builder.add_node(
#     "rag",
#     rag_node
# )

# builder.add_node(
#     "conversation",
#     conversation_node
# )

# builder.add_node(
#     "lead_qualification",
#     lead_qualification_node
# )

# builder.add_node(
#     "analytics",
#     analytics_node
# )

# # Entry
# builder.add_edge(
#     START,
#     "call_init"
# )

# builder.add_edge(
#     "call_init",
#     "intent_router"
# )

# # Conditional Routing
# builder.add_conditional_edges(
#     "intent_router",
#     route_after_intent,
#     {
#         "rag": "rag",
#         "conversation": "conversation"
#     }
# )

# # RAG Path
# builder.add_edge(
#     "rag",
#     "conversation"
# )

# # Post Conversation
# builder.add_edge(
#     "conversation",
#     "lead_qualification"
# )

# builder.add_edge(
#     "lead_qualification",
#     "analytics"
# )

# builder.add_edge(
#     "analytics",
#     END
# )

# graph = builder.compile()

# graph.py
from langgraph.graph import StateGraph, START, END
from state import AgentState
from intent_router_node import intent_router_node
from rag_node import rag_node
from conversation_node import conversation_node
from lead_qualification_node import lead_qualification_node
from analytics_node import analytics_node

def route_after_intent(state: AgentState):
    if state["requires_rag"]:
        return "rag"
    return "conversation"

builder = StateGraph(AgentState)

# Notice call_init is removed. The graph handles one turn at a time.
builder.add_node("intent_router", intent_router_node)
builder.add_node("rag", rag_node)
builder.add_node("conversation", conversation_node)
builder.add_node("lead_qualification", lead_qualification_node)
builder.add_node("analytics", analytics_node)

# Entry point is now the intent router
builder.add_edge(START, "intent_router")

builder.add_conditional_edges(
    "intent_router",
    route_after_intent,
    {
        "rag": "rag",
        "conversation": "conversation"
    }
)

builder.add_edge("rag", "conversation")
builder.add_edge("conversation", "lead_qualification")
builder.add_edge("lead_qualification", "analytics")
builder.add_edge("analytics", END)

graph = builder.compile()