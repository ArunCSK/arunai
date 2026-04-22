import os
import json
import backoff
from ddgs import DDGS
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# Configuration
KNOWLEDGE_DIR = "knowledge"

class SessionState:
    def __init__(self):
        self.selected_agent = "gemini-2.5-flash-lite" # Default
        self.history = []
        self.last_search_results = ""

def get_available_gemini_models():
    """Returns a list of likely available Gemini models."""
    return [
        "gemini-2.5-flash-lite",
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-1.0-pro"
    ]

def internet_search(query: str, max_results=5):
    """Performs a search using DuckDuckGo and returns formatted results."""
    print(f"Searching internet for: '{query}'...")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            if not results:
                return "No results found."
            
            formatted = []
            for r in results:
                formatted.append(f"Title: {r['title']}\nSnippet: {r['body']}\nSource: {r['href']}")
            
            return "\n\n".join(formatted)
    except Exception as e:
        return f"Search failed: {e}"

@backoff.on_exception(backoff.expo, Exception, max_tries=5)
def safe_generate_content(client, model, contents, config):
    """Wrapper with exponential backoff for Gemini generation."""
    return client.models.generate_content(model=model, contents=contents, config=config)

def select_agent():
    """CLI prompt to select a Gemini agent."""
    models = get_available_gemini_models()
    print("\n--- Available Gemini Agents ---")
    for i, model in enumerate(models):
        print(f"{i + 1}. {model}")
    
    default_index = 1 # gemini-2.5-flash-lite
    
    choice = input(f"\nSelect an agent (1-{len(models)}, default {default_index}): ").strip()
    
    if not choice:
        return models[default_index - 1]
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(models):
            return models[idx]
    except ValueError:
        pass
    
    print(f"Invalid choice. Using default: {models[default_index - 1]}")
    return models[default_index - 1]

def run_rag_internet_search():
    # Load keys
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY or GOOGLE_API_KEY environment variable is not set.")
        return

    client = genai.Client(api_key=api_key)
    state = SessionState()
    state.selected_agent = select_agent()
    
    print(f"\n--- RAG Internet Search Active ({state.selected_agent}) ---")
    print("Type 'exit' to quit, 'explain' for details on the last answer.")

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
            
        if not user_input:
            continue
            
        if user_input.lower() in ["exit", "quit"]:
            break

        if user_input.lower() in ["explain", "more details", "explain more", "details"]:
            if not state.last_search_results:
                print("Gemini: I haven't searched for anything yet. Please ask a question first.")
                continue
            
            print("Providing detailed explanation based on last search...")
            explanation_prompt = f"Based on these search results, provide a detailed explanation:\n\n{state.last_search_results}"
            
            try:
                response = safe_generate_content(
                    client,
                    model=state.selected_agent,
                    contents=explanation_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction="You are a helpful assistant providing detailed explanations."
                    )
                )
                print(f"\nGemini: {response.text}")
            except Exception as e:
                print(f"Error: {e}")
            continue

        # Normal Search RAG Flow
        search_results = internet_search(user_input)
        state.last_search_results = search_results
        
        system_instruction = (
            "You are a helpful assistant. Use the provided search results to answer the user's question. "
            "CRITICAL: Your answer MUST be exactly 2 to 3 lines long. Be concise and direct."
        )
        
        full_prompt = f"Search Results:\n{search_results}\n\nUser Question: {user_input}"

        try:
            response = safe_generate_content(
                client,
                model=state.selected_agent,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction
                )
            )
            print(f"\nGemini: {response.text}")
        except Exception as e:
            if "429" in str(e):
                print(f"\nError: Model '{state.selected_agent}' is rate-limited.")
                print("Tip: Try selecting a different model next time.")
            else:
                print(f"Error: {e}")

if __name__ == "__main__":
    run_rag_internet_search()
