# cli_chat.py
import json
from state import AgentState
from call_init_node import call_init_node
from graph import graph

def main():
    print("Initializing Ezora Voice Agent...")
    
    # 1. Bootstrap the initial state outside the graph
    empty_state = {}
    current_state = call_init_node(empty_state)
    
    print(f"\nAssistant: {current_state['assistant_message']}")

    # 2. Start the continuous conversation loop
    while True:
        try:
            user_input = input("\nUser: ")
            if user_input.lower() in ["quit", "exit"]:
                break
                
            # Update state with the new user message
            current_state["user_message"] = user_input
            
            # Invoke the graph for this single turn
            current_state = graph.invoke(current_state)
            
            # Print the required debugging information
            print("\n--- Turn Debug Info ---")
            print(f"Intent: {current_state.get('intent')}")
            print(f"Rewritten Query: {current_state.get('rewritten_query')}")
            print(f"Lead Data: {json.dumps(current_state.get('lead_data'), indent=2)}")
            print(f"Lead Score: {current_state.get('lead_score')}")
            print("-----------------------\n")
            
            print(f"Assistant: {current_state['assistant_message']}")
            
            # Check if the analytics node flagged the call as completed
            if current_state.get("call_completed"):
                print("\n[Call Ended]")
                print(f"Final Outcome: {current_state.get('call_outcome')}")
                print(f"Final Sentiment: {current_state.get('sentiment')}")
                break
                
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()