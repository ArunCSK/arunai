import asyncio
import os
import sys
import anyio

# Attempt to import necessary modules
try:
    from claude_agent_sdk import query, ClaudeAgentOptions
    from claude_agent_sdk.types import PermissionResultAllow, PermissionResultDeny
except ImportError:
    print("Error: The 'claude-agent-sdk' package is required.")
    sys.exit(1)

# Ensure LiteLLM is pointing to Gemini
os.environ["ANTHROPIC_BASE_URL"] = "http://localhost:4000"
os.environ["ANTHROPIC_API_KEY"] = "sk-placeholder-key"

async def ask_user_callback(tool_name, tool_input, context):
    """
    Auto-approve safe retrieval tools (Grep/Read).
    Explicitly ask for 'Write' or 'Bash' to satisfy user permission requirement.
    """
    safe_retrieval_tools = ["Grep", "Glob", "Read", "ListFiles"]
    if tool_name in safe_retrieval_tools:
        return PermissionResultAllow()
    
    # Triggered for Write, Bash, etc.
    print(f"\n" + "="*40)
    print(f"🚨 PERMISSION REQUEST: {tool_name}")
    print(f"="*40)
    print(f"Action: The agent wants to modify your files or run a command.")
    print(f"Details: {tool_input}")
    print("-" * 40)
    
    prompt = "Allow this action? (y/n/q to quit): "
    while True:
        try:
            # Use anyio.to_thread.run_sync to avoid blocking the event loop
            confirm = await anyio.to_thread.run_sync(input, prompt)
            confirm = confirm.lower().strip()
            if confirm == 'y':
                print("Action allowed.")
                return PermissionResultAllow()
            elif confirm == 'n':
                print("Action denied.")
                return PermissionResultDeny(message="The user explicitly denied this file creation/action.")
            elif confirm == 'q':
                print("Exiting...")
                sys.exit(0)
            else:
                print("Invalid input. Please enter 'y', 'n', or 'q'.")
        except EOFError:
            return PermissionResultDeny(message="Input stream closed.")

async def prompt_generator(text):
    """
    Yields the prompt as an AsyncIterable. Required for can_use_tool callback.
    """
    yield {
        "type": "user",
        "message": {"role": "user", "content": text}
    }

async def run_rag_agent():
    # Capture user prompt interactively
    print("\n" + "="*50)
    print("🤖 INTERACTIVE RAG AGENT")
    print("="*50)
    user_query = input("🔎 What would you like to know from the knowledge base? ")
    
    if not user_query:
        print("Empty query. Exiting.")
        return

    print(f"\n--- Processing Query: '{user_query}' ---")
    
    options = ClaudeAgentOptions(
        model="claude-3-5-sonnet-20241022", 
        can_use_tool=ask_user_callback,
        allowed_tools=["Grep", "Glob", "Read", "Write", "Bash"],
        cwd=os.getcwd()
    )

    # Instruct the agent to:
    # 1. Search knowledge/
    # 2. Answer the user
    # 3. Save a summary to a file (requires permission)
    system_instructions = (
        "You are a local RAG agent. Step 1: Search the 'knowledge/' folder "
        "to find facts related to the user's question. Step 2: Answer the question "
        "honestly based on the files. Step 3: Summarize your findings and "
        "SAVE the summary to a new file named 'rag_summary.txt' in the current directory."
    )
    
    full_prompt = f"{system_instructions}\n\nUser Question: {user_query}"

    try:
        async for message in query(prompt=prompt_generator(full_prompt), options=options):
            # Handle text thoughts and answers
            if hasattr(message, "content"):
                for block in message.content:
                    if hasattr(block, "text") and block.text:
                        print(f"\n🤖 Agent: {block.text}")
            
            # Handle tool output (retrieval steps)
            if hasattr(message, "result"):
                res_str = str(message.result)
                if len(res_str) > 150:
                    res_str = res_str[:150] + "... [truncated]"
                print(f"🔧 Tool Result: {res_str}")

        print("\n✅ Task completed.")

    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(run_rag_agent())
    except KeyboardInterrupt:
        print("\nExiting...")
