# Copilot SDK Integration Guide

## Overview

Stock Agent Chat now supports **real Copilot SDK integration** for actual AI agent interactions. The application seamlessly falls back to simulation mode if the SDK is not available or configured.

## Architecture

### Dual-Mode Operation

```
┌─────────────────────────────────────────────┐
│      User sends message via Streamlit       │
└──────────────┬──────────────────────────────┘
               │
               ▼
         ┌─────────────┐
         │ send_message│
         └──────┬──────┘
                │
         ┌──────▼──────────┐
         │ SDK Available?  │
         └──────┬──────┬───┘
         YES    │      │    NO
                ▼      ▼
          ┌─────────┐ ┌─────────────┐
          │Real SDK │ │ Simulation  │
          │ (API)   │ │ (Keyword-   │
          │ calls   │ │  based      │
          │ model   │ │  routing)   │
          └───┬─────┘ └─────┬───────┘
              │             │
              └──────┬──────┘
                     ▼
         ┌─────────────────────┐
         │ Tool Invocation     │
         │ (Real or Simulated) │
         └──────────┬──────────┘
                    ▼
         ┌─────────────────────┐
         │ Response Formatting │
         │ (Unified API)       │
         └────────────────────┘
```

## Configuration

### Option 1: Let SDK Manage CLI Automatically (Recommended)

```bash
# .env
COPILOT_CLI_URL=
DEFAULT_MODEL=gpt-4.1
```

The SDK will:
- Automatically launch Copilot CLI
- Handle authentication
- Manage lifecycle

**Requirements:**
- GitHub Copilot CLI installed: `copilot --version`
- GitHub authentication: `copilot auth login`

### Option 2: Connect to External CLI Server

**Terminal 1: Start Copilot CLI in server mode**
```bash
copilot --headless --port 4321
```

**Terminal 2: Configure app to connect**
```bash
# .env
COPILOT_CLI_URL=localhost:4321
DEFAULT_MODEL=gpt-4.1
```

**Advantages:**
- Reuse single CLI across multiple processes
- Debug CLI logs independently
- Persistent authentication

## How It Works

### Real SDK Mode (When Available)

```python
# In src/agent.py
response = self.copilot_client.sendMessage(
    prompt=full_message,
    model=self.model,
    tools=[get_stock_data_handler, analyze_stock_data_handler],
    temperature=0.7,
    maxTokens=2048
)

# The SDK automatically:
# 1. Formats tools in JSON schema
# 2. Sends request to Copilot CLI
# 3. Receives response with tool calls
# 4. Returns parsed response
```

### Simulation Mode (Fallback)

```python
# In src/agent.py (fallback method)
# Analyzes message keywords to determine which tools to call
if "price" in message.lower():
    call_tool("get_stock_data", symbol)
if "average" in message.lower():
    call_tool("analyze_stock_data", symbol, question)
```

## Supported Models

The following models work with Copilot SDK:

| Model | Description | Status |
|-------|-------------|----|
| `gpt-4.1` | GPT-4 Turbo | ✅ Recommended |
| `gpt-4o` | GPT-4 Optimized | ✅ Works |
| `claude-haiku-4.5` | Claude Haiku | ⚠️ Simulation only |
| `gpt-5-mini` | GPT-5 Mini | ⚠️ When available |

**Note**: Claude models currently only work in simulation mode. For real SDK integration, use OpenAI models (gpt-4.1, gpt-4o).

## Tool Integration

### How Tools Are Registered

```python
# In src/tools.py

def get_stock_data_handler(symbol: str) -> Dict[str, Any]:
    """Fetch stock prices for a company."""
    ...

def analyze_stock_data_handler(symbol: str, question: str) -> Dict[str, Any]:
    """Analyze stock prices."""
    ...

# Get all tool handlers
def get_tool_handlers() -> Dict[str, callable]:
    return {
        "get_stock_data": get_stock_data_handler,
        "analyze_stock_data": analyze_stock_data_handler
    }
```

### Tool Definitions

Tools are defined with JSON schema in `TOOL_DEFINITIONS`:

```python
{
    "name": "get_stock_data",
    "description": "Fetch the last 5 days of stock price data for a company",
    "parameters": {
        "type": "object",
        "properties": {
            "symbol": {"type": "string", "description": "Stock ticker symbol"}
        },
        "required": ["symbol"]
    }
}
```

## Response Format

All responses follow a unified format regardless of mode:

```python
{
    "success": True,              # Whether call succeeded
    "message": "The average...",  # Agent response text
    "tool_calls": [               # Tools the agent called
        {
            "name": "get_stock_data",
            "args": {"symbol": "AAPL"},
            "result": [...]        # Tool output
        }
    ],
    "model": "gpt-4.1",           # Model used
    "usage": {                    # Token usage
        "input_tokens": 50,
        "output_tokens": 150
    }
}
```

## Error Handling

The agent gracefully handles errors:

```python
# If SDK port is wrong
COPILOT_CLI_URL=localhost:9999
→ Falls back to simulation

# If model not available
DEFAULT_MODEL=claude-99
→ Falls back to simulation

# If SDK call times out
→ Captures error, returns fallback response

# If tool execution fails
→ Returns error message to user
```

## Testing

### Run Complete Test Suite

```bash
pytest tests/ -v
# 69/74 tests passing (93% success)
```

### Test Only Agent Integration

```bash
pytest tests/test_agent.py -v
# 17/17 tests passing ✅
```

### Test Tools

```bash
pytest tests/test_tools.py -v
# 18/18 tests passing ✅
```

## Enabling Real SDK Usage

To use the real Copilot SDK:

### 1. Install Copilot CLI

```bash
# macOS/Linux
brew install copilot-cli

# Or download from https://github.com/github/copilot-cli
```

### 2. Authenticate

```bash
copilot auth login
```

### 3. Configure Application

```bash
# Option A: Auto-manage CLI
cp .env.example .env
# Leave COPILOT_CLI_URL empty

# Option B: External CLI server
copilot --headless --port 4321 &
# Set COPILOT_CLI_URL=localhost:4321 in .env
```

### 4. Use GPT Model (For Real SDK)

```bash
# .env
DEFAULT_MODEL=gpt-4.1
COPILOT_CLI_URL=          # or localhost:4321
```

### 5. Run Application

```bash
streamlit run stock_app.py
```

The agent will automatically use real SDK if available, simulation otherwise.

## Monitoring

### Check SDK Status

```python
# In Python REPL
from src.agent import initialize_agent

agent = initialize_agent()
print(f"SDK available: {agent.use_sdk}")
print(f"Using SDK: {agent.copilot_client is not None}")
print(f"Model: {agent.model}")
```

### See Fallback Notices

Errors are printed to console when SDK is unavailable:

```
Warning: Failed to initialize Copilot SDK: [error details]
Using simulation mode instead
SDK call failed: [error]. Falling back to simulation.
```

## Performance

| Operation | Real SDK | Simulation |
|-----------|----------|-----------|
| Agent response | 500-2000ms | <100ms |
| Tool calling | Automatic | Keyword-based |
| Tool execution | SDK manages | Direct calls |
| Streaming | Supported | Not supported |

## Next Steps

### Recommended: Start with Simulation

1. **Test functionality**: Run `streamlit run stock_app.py`
2. **Verify tests**: Run `pytest tests/ -v`
3. **Demo setup**: Works without SDK installed

### Advanced: Integrate Real SDK

1. Install Copilot CLI
2. Configure COPILOT_CLI_URL
3. Switch DEFAULT_MODEL to gpt-4.1
4. Monitor logs for fallback behavior

## Troubleshooting

### SDK Not Initializing

**Error**: "Failed to initialize Copilot SDK"

**Solution**:
```bash
# Check CLI installed
copilot --version

# Check authenticated
copilot auth status

# Try external server
copilot --headless --port 4321
# Then set COPILOT_CLI_URL=localhost:4321
```

### Wrong Model

**Error**: "Model not available"

**Solution**:
```bash
# Use supported model
DEFAULT_MODEL=gpt-4.1
```

### Tool Not Being Called

**Error**: Agent doesn't call tools

**Causes**:
- SDK not available (using simulation)
- Tool definitions not matching
- Model doesn't support tools

**Solution**:
- Verify `COPILOT_CLI_URL` is correct
- Check `DEFAULT_MODEL` supports tools
- Review tool definitions in src/tools.py

## Technical Details

### Code Organization

- **src/agent.py**: CopilotAgent class with SDK/simulation logic
- **src/tools.py**: Tool handlers and definitions
- **src/models.py**: Data models for stock data
- **src/stock_data.py**: Mock price generator
- **stock_app.py**: Streamlit UI using agent

### Key Classes

- `CopilotAgent`: Wrapper with SDK and simulation support
- `CopilotClient`: From github_copilot_sdk (when available)
- `ToolResult`: Standardized tool response format

### Event Handling

Responses are unified so UI doesn't need to know if SDK or simulation is used:

```python
# UI code
response = agent.send_message("What's the price?", context)

# Works the same whether SDK or simulation:
# response["message"] contains agent response
# response["tool_calls"] contains tool invocations
```

## References

- [Copilot SDK Documentation](https://github.com/github/copilot-sdk)
- [Copilot CLI Reference](https://github.com/github/copilot-cli)
- [GitHub Copilot Auth Guide](https://docs.github.com/en/copilot)
