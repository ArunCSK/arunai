import os
import litellm
import json
import backoff
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Configuration
KNOWLEDGE_DIR = "knowledge"

def get_knowledge_files() -> List[str]:
    """Returns a list of all text files in the knowledge directory."""
    if not os.path.exists(KNOWLEDGE_DIR):
        return []
    return [f for f in os.listdir(KNOWLEDGE_DIR) if f.endswith(".txt")]

def search_knowledge(query: str) -> str:
    """
    Searches the local knowledge base for relevant information.
    Handles UTF-16 LE encoding.
    """
    files = get_knowledge_files()
    context = []
    for filename in files:
        path = os.path.join(KNOWLEDGE_DIR, filename)
        try:
            with open(path, "r", encoding="utf-16") as f:
                content = f.read()
                if query.lower() in content.lower() or query.lower() in filename.lower():
                    context.append(f"--- File: {filename} ---\n{content}")
        except Exception as e:
            pass
    
    if not context:
        for filename in files:
            path = os.path.join(KNOWLEDGE_DIR, filename)
            try:
                with open(path, "r", encoding="utf-16") as f:
                    context.append(f"--- File: {filename} ---\n{f.read()}")
            except:
                pass
                
    return "\n\n".join(context)

# Define the tool for LiteLLM
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge",
            "description": "Search the local knowledge base for project and team information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to find relevant information."
                    }
                },
                "required": ["query"]
            }
        }
    }
]

@backoff.on_exception(backoff.expo, (litellm.RateLimitError, litellm.ServiceUnavailableError), max_tries=5)
def safe_completion(**kwargs):
    """Wrapper with exponential backoff for rate limits and service busy errors."""
    return litellm.completion(**kwargs)

def run_gemini_agent():
    # Load keys
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY or GOOGLE_API_KEY environment variable is not set.")
        return

    # Clean up the Proxy URL (remove any quotes and fix 0.0.0.0 for Windows)
    PROXY_URL = os.environ.get("LITELLM_PROXY_URL")
    if PROXY_URL:
        PROXY_URL = PROXY_URL.strip("'\"").replace("0.0.0.0", "127.0.0.1")

    print("\n--- Gemini RAG Agent with LiteLLM ---")
    if PROXY_URL:
        print(f"Using LiteLLM Proxy at: {PROXY_URL}")
    print(f"Knowledge directory: {KNOWLEDGE_DIR}")
    
    # Preferred model identifiers
    MODELS_TO_TRY = [
        "gemini/gemini-1.5-flash",
        "gemini/gemini-1.5-pro",
        "gemini/gemini-1.0-pro"
    ]
    
    current_model = MODELS_TO_TRY[0]
    messages = [
        {"role": "system", "content": "You are a helpful assistant that uses the local knowledge base to answer user questions. If you don't know something, use the search_knowledge tool."}
    ]

    while True:
        try:
            user_input = input("\nYou: ")
        except (EOFError, KeyboardInterrupt):
            break
            
        if user_input.lower() in ["exit", "quit"]:
            break

        messages.append({"role": "user", "content": user_input})

        try:
            response = None
            working_kwargs = {}
            
            for model in MODELS_TO_TRY:
                try:
                    completion_kwargs = {
                        "model": model,
                        "messages": messages,
                        "tools": tools,
                        "tool_choice": "auto"
                    }
                    
                    if PROXY_URL:
                        completion_kwargs["api_base"] = PROXY_URL
                        completion_kwargs["api_key"] = "sk-placeholder"
                    
                    try:
                        response = safe_completion(**completion_kwargs)
                        working_kwargs = completion_kwargs
                    except Exception as e:
                        if PROXY_URL:
                            print(f"⚠️ Proxy failed for {model}, retrying directly...")
                            completion_kwargs.pop("api_base", None)
                            completion_kwargs["api_key"] = api_key
                            response = safe_completion(**completion_kwargs)
                            working_kwargs = completion_kwargs
                        else:
                            raise e

                    current_model = model
                    break
                except Exception as e:
                    if "404" in str(e) or "not found" in str(e).lower():
                        continue
                    print(f"❌ {model} failed: {e}")
                    continue
            
            if not response:
                print("❌ Error: All attempted models failed. Check your API key or try again later.")
                break

            response_message = response.choices[0].message
            messages.append(response_message)

            if response_message.get("tool_calls"):
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    if function_name == "search_knowledge":
                        print(f"🔧 Searching knowledge base for: '{function_args.get('query')}'")
                        tool_result = search_knowledge(function_args.get("query"))
                        
                        messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": tool_result,
                        })

                # Follow up call
                followup_kwargs = {
                    "model": current_model,
                    "messages": messages
                }
                if working_kwargs.get("api_base"):
                    followup_kwargs["api_base"] = working_kwargs["api_base"]
                    followup_kwargs["api_key"] = working_kwargs["api_key"]
                
                second_response = safe_completion(**followup_kwargs)
                final_message = second_response.choices[0].message
                print(f"\nGemini: {final_message.content}")
                messages.append(final_message)
            else:
                print(f"\nGemini: {response_message.content}")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_gemini_agent()
