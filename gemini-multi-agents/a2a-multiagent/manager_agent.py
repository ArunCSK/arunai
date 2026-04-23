import os
import requests
import uuid
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Explicitly fetch the API key to handle missing cases better
api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

if not api_key:
    print("\n[Manager Error] No API key found in the environment!")
    print("Please ensure you have a '.env' file in this directory with:")
    print("GEMINI_API_KEY=your_actual_api_key_here")
    print("Or set the environment variable GOOGLE_API_KEY.")
    exit(1)

# Initialize Gemini Client with the explicit key
client = genai.Client(api_key=api_key)

WORKER_AGENT_URL = "http://127.0.0.1:8000"

def discover_agent(base_url):
    """
    Step 1 of A2A Protocol: Discovery.
    The Client asks the Server for its Agent Card to understand its capabilities.
    """
    try:
        response = requests.get(f"{base_url}/.well-known/agent-card.json")
        response.raise_for_status()
        card = response.json()
        print(f"[Manager] Discovered Agent: {card['agent_name']}")
        print(f"[Manager] Capabilities: {', '.join(card['capabilities'])}")
        return card
    except requests.exceptions.RequestException as e:
        print(f"[Manager] Failed to discover agent at {base_url}. Error: {e}")
        return None

def delegate_task(base_url, task_endpoint, instruction, data=""):
    """
    Step 2 of A2A Protocol: Task Execution.
    The Client delegates a specific task to the Worker Agent.
    """
    task_id = str(uuid.uuid4())
    print(f"\n[Manager] Delegating Task {task_id} to {base_url}...")
    
    payload = {
        "task_id": task_id,
        "instruction": instruction,
        "data": data
    }
    
    try:
        response = requests.post(f"{base_url}{task_endpoint}", json=payload)
        response.raise_for_status()
        result = response.json()
        print(f"[Manager] Task Completed successfully.")
        return result['result']
    except requests.exceptions.RequestException as e:
        print(f"[Manager] Failed to execute task. Error: {e}")
        if response is not None:
             print(f"Server returned: {response.text}")
        return None

def main():
    print("=== Multi-Agent Orchestration Started ===")
    
    # The overall goal the user gave the Manager Agent
    user_goal = "I need a summary of the latest AI trends, but also give me a critical analysis of its limitations."
    raw_data = """
    AI is advancing rapidly. Large Language Models (LLMs) are becoming multimodal, 
    processing text, image, and audio natively. There's a shift from just chatting 
    with AI to using AI Agents that take actions on behalf of the user. However, 
    hallucinations remain a problem. AI systems also struggle with complex reasoning 
    over long horizons and consume massive amounts of energy for training and inference. 
    Data privacy and copyright issues are currently heavily debated.
    """
    
    print(f"[Manager] User Goal: {user_goal}")
    
    # 1. Discover the worker
    worker_card = discover_agent(WORKER_AGENT_URL)
    
    if not worker_card:
        print("[Manager] Could not proceed without the worker agent. Please ensure it is running.")
        return

    # 2. Planning (Manager Agent decides what to do)
    # The manager uses Gemini to break down the task
    print("\n[Manager] Planning... (Thinking with Gemini)")
    
    manager_prompt = f"""
    You are the Manager Agent. You have a Worker Agent with the following capabilities:
    {json.dumps(worker_card, indent=2)}
    
    User Goal: {user_goal}
    
    Decide how to split the work. The Worker Agent should do the heavy lifting of data analysis.
    Write a specific instruction to send to the Worker Agent to accomplish the user's goal based on its capabilities.
    Output ONLY the instruction text you want to send to the Worker Agent.
    """
    
    try:
        plan_response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=manager_prompt,
        )
        worker_instruction = plan_response.text.strip()
        print(f"[Manager] Decided to delegate this instruction: '{worker_instruction}'")
    except Exception as e:
        print(f"Error calling Gemini for planning: {e}")
        return
    
    # 3. Execution (Delegate to Worker)
    worker_result = delegate_task(
        base_url=WORKER_AGENT_URL, 
        task_endpoint=worker_card['endpoints']['tasks'], 
        instruction=worker_instruction, 
        data=raw_data
    )
    
    if not worker_result:
         return
         
    print(f"\n[Worker Result]:\n{worker_result}")
    
    # 4. Final Synthesis
    print("\n[Manager] Synthesizing final response...")
    
    synthesis_prompt = f"""
    The user asked for: "{user_goal}"
    
    The Worker Agent provided this analysis:
    "{worker_result}"
    
    Write the final response to the user, formatting it nicely.
    """
    
    try:
        final_response = client.models.generate_content(
             model='gemini-2.0-flash',
             contents=synthesis_prompt
        )
        print("\n=== Final Output ===")
        print(final_response.text)
    except Exception as e:
        print(f"Error calling Gemini for synthesis: {e}")


if __name__ == "__main__":
    main()
