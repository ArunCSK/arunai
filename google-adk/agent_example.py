import asyncio
import os
import sys
import anyio

# Attempt to import necessary modules
try:
    from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
    from claude_agent_sdk.types import PermissionResultAllow, PermissionResultDeny
except ImportError:
    print("Error: The 'claude-agent-sdk' package is required.")
    sys.exit(1)

# Configuration
os.environ["ANTHROPIC_BASE_URL"] = "http://localhost:4000"
os.environ["ANTHROPIC_API_KEY"] = "sk-placeholder-key"

async def ask_user_callback(tool_name, tool_input, context):
    """Callback to intercept tool executions and ask for permission."""
    print(f"\n" + "="*40)
    print(f"🚨 PERMISSION REQUEST: {tool_name}")
    print(f"="*40)
    print(f"Input: {tool_input}")
    print("-" * 40)
    
    prompt = "Allow this action? (y/n/q to quit): "
    while True:
        try:
            # Non-blocking input handling
            confirm = await anyio.to_thread.run_sync(input, prompt)
            confirm = confirm.lower().strip()
            if confirm == 'y':
                return PermissionResultAllow()
            elif confirm == 'n':
                return PermissionResultDeny(message="User denied.")
            elif confirm == 'q':
                sys.exit(0)
        except EOFError:
            return PermissionResultDeny(message="Input closed.")

async def run_agent():
    print("--- Starting Agent ---")
    print(f"Connecting to LiteLLM at {os.environ['ANTHROPIC_BASE_URL']}...")
    
    options = ClaudeAgentOptions(
        model="claude-3-5-sonnet-20241022", 
        can_use_tool=ask_user_callback,
        allowed_tools=["Bash", "Glob", "Read", "Write", "Edit"],
        cwd=os.getcwd()
    )

    text_prompt = "Create a file named 'hello_gemini.txt' and write 'Hello from Gemini!' inside."

    try:
        # Using ClaudeSDKClient as an async context manager
        async with ClaudeSDKClient(options) as client:
            print("DEBUG: Client connected. Initiating query...")
            
            # The client.query() method starts the task and must be awaited.
            # It does not return the stream itself.
            await client.query(text_prompt)
            
            print("DEBUG: Query initiated. Consuming response stream...")
            
            # Use receive_response() to iterate over the messages from the agent.
            async for message in client.receive_response():
                # Handle Assistant Messages (thoughts and replies)
                if hasattr(message, "content"):
                    for block in message.content:
                        if hasattr(block, "text") and block.text:
                            print(f"\n🤖 Agent: {block.text}")
                
                # Handle Tool results (what happened after you clicked 'y')
                if hasattr(message, "result"):
                    print(f"🔧 Tool Result: {str(message.result)[:150]}...")

    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        print("\nTip: Ensure your LiteLLM proxy is running: 'litellm --model gemini/gemini-1.5-pro'")

if __name__ == "__main__":
    try:
        asyncio.run(run_agent())
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
