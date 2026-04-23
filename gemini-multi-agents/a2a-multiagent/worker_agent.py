import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Explicitly fetch the API key to handle missing cases better
api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

if not api_key:
    print("\n[Worker Error] No API key found in the environment!")
    print("Please ensure you have a '.env' file in this directory with:")
    print("GEMINI_API_KEY=your_actual_api_key_here")
    print("Or set the environment variable GOOGLE_API_KEY.")
    exit(1)

# Initialize Gemini Client with the explicit key
client = genai.Client(api_key=api_key)

app = FastAPI(title="Worker Agent - A2A Protocol Simulation")

class TaskRequest(BaseModel):
    task_id: str
    instruction: str
    data: str = ""

class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: str

# 1. The Agent Card (Discovery)
# This is a core concept of the A2A protocol. It tells other agents what this agent can do.
@app.get("/.well-known/agent-card.json")
def get_agent_card():
    return {
        "agent_name": "DataAnalyzerAgent",
        "description": "An agent that specializes in analyzing text data, extracting key themes, and providing concise summaries.",
        "capabilities": ["text-analysis", "summarization"],
        "endpoints": {
            "tasks": "/tasks"
        },
        "protocol_version": "A2A/1.0"
    }

# 2. The Task Execution Endpoint
# In A2A, clients send tasks rather than direct prompts.
@app.post("/tasks", response_model=TaskResponse)
def execute_task(request: TaskRequest):
    print(f"[Worker] Received task {request.task_id}: {request.instruction}")
    
    prompt = f"Instruction: {request.instruction}\n\nData: {request.data}\n\nPlease perform the instruction on the data."
    
    try:
        # Use Gemini to perform the actual task
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
        )
        
        return TaskResponse(
            task_id=request.task_id,
            status="completed",
            result=response.text
        )
    except Exception as e:
        print(f"[Worker] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("Starting Worker Agent on port 8000...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
