import json
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from typing import Dict, Any

from state import AgentState
from call_init_node import call_init_node
from graph import graph

app = FastAPI(
    title="Ezora Voice Agent API",
    description="WebSocket Backend for Real-Time Voice"
)

# 1. Add this route to serve your index.html page
@app.get("/")
async def serve_frontend():
    # Make sure your index.html file is in the same directory
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {"error": "index.html not found. Please add it to the root directory."}


# 2. Your existing WebSocket route
@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
  
    await websocket.accept()
    print("New call connected via WebSocket.")
    
    empty_state = {}
    current_state = call_init_node(empty_state)
    
    await websocket.send_json({
        "type": "greeting",
        "assistant_message": current_state["assistant_message"]
    })
    
    try:
        while True:
            data = await websocket.receive_text()
            
            current_state["user_message"] = data
            
            # Invoke the graph 
            current_state = graph.invoke(current_state)
            
            # Send the AI's response and current lead data back to the client
            await websocket.send_json({
                "type": "response",
                "assistant_message": current_state["assistant_message"],
                "lead_data": current_state.get("lead_data", {}),
                "lead_score": current_state.get("lead_score", 0)
            })
            
            if current_state.get("call_completed"):
                total_turns = len(current_state.get("messages", [])) // 2 
                
                call_record = {
                    "call_id": current_state.get("call_id"),
                    "session_id": current_state.get("session_id"),
                    "timestamp": current_state.get("timestamp"),
                    "total_turns": total_turns,
                    "final_intent": current_state.get("intent"),
                    "lead_profile": current_state.get("lead_data"),
                    "lead_score": current_state.get("lead_score"),
                    "customer_sentiment": current_state.get("sentiment"),
                    "call_outcome": current_state.get("call_outcome")
                }
                
                print("\n=== CALL TERMINATED: FINAL DATA RECORD ===")
                print(json.dumps(call_record, indent=2))
                print("==========================================\n")
                
                print("Call completed naturally. Closing connection.")
                await websocket.close()
                break
                
    except WebSocketDisconnect:
        print("\nClient disconnected unexpectedly. Saving partial state to DB...")