from pprint import pprint

from graph import graph


def main():

    initial_state = {

        # Call Info
        "call_id": "",
        "session_id": "",
        "phone_number": "+919999999999",

        # Current Turn
        "user_message":
            "Do you integrate with Salesforce?",

        "assistant_message": "",

        # History
        "messages": [],

        # Intent
        "intent": None,
        "intent_confidence": 0.0,
        "rewritten_query": "",

        # RAG
        "retrieved_docs": [],
        "context": "",

        # Routing
        "requires_rag": False,
        "requires_human": False,
        "need_qualification": False,
        "need_end_call": False,

        # Lead Qualification
        "lead_data": {},
        "lead_score": 0,

        # Analytics
        "sentiment": None,
        "call_outcome": None,

        # Conversation
        "current_stage": "greeting",

        # Metadata
        "timestamp": "",

        "system_prompt": "",

        "qualification_stage": "industry"
    }

    result = graph.invoke(
        initial_state
    )

    print("\n" + "=" * 50)
    print("FINAL STATE")
    print("=" * 50)

    pprint(result)

    print("\nAssistant Response:\n")
    print(
        result["assistant_message"]
    )

    print("\nIntent:")
    print(
        result["intent"]
    )

    print("\nLead Score:")
    print(
        result["lead_score"]
    )

    print("\nSentiment:")
    print(
        result["sentiment"]
    )

    print("\nCall Outcome:")
    print(
        result["call_outcome"]
    )


if __name__ == "__main__":
    main()