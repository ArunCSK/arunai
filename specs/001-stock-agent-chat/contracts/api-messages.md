# API Message Contracts: Stock Agent Chat Application

**Phase**: Phase 1 - Design  
**Date**: February 26, 2026  
**Feature**: [001-stock-agent-chat](../spec.md)

## Chat Message Format

All messages in the application follow a consistent format for serialization and display.

### User Message Format

```json
{
  "sender": "user",
  "content": "What is the average price of AAPL?",
  "timestamp": "2026-02-26T14:30:00Z",
  "tool_calls": null
}
```

**Fields**:
- `sender`: Always "user" for user-sent messages
- `content`: Plain text user question or statement
- `timestamp`: ISO 8601 UTC timestamp (use `datetime.now(timezone.utc).isoformat()`)
- `tool_calls`: Always null for user messages

**Constraints**:
- content: 1-4096 characters
- timestamp: Valid ISO 8601 format
- sender: String "user" (case-sensitive)

---

### Agent Response Message Format

```json
{
  "sender": "agent",
  "content": "The average price of AAPL over 5 days is $151.96, calculated from the closing prices.",
  "timestamp": "2026-02-26T14:30:05Z",
  "tool_calls": [
    {
      "name": "get_stock_data",
      "args": {
        "symbol": "AAPL"
      },
      "result": [
        {
          "date": "2026-02-22",
          "open": 150.0,
          "close": 151.5,
          "high": 152.0,
          "low": 149.5
        },
        {
          "date": "2026-02-23",
          "open": 151.5,
          "close": 152.8,
          "high": 153.5,
          "low": 151.0
        }
      ]
    }
  ]
}
```

**Fields**:
- `sender`: Always "agent" for AI agent responses
- `content`: Agent's natural language response
- `timestamp`: ISO 8601 UTC timestamp
- `tool_calls`: Array of tool invocations (can be empty if no tools called)

**Tool Call Object**:
- `name`: Tool name (e.g., "get_stock_data", "analyze_stock_data")
- `args`: Object with the arguments passed to the tool
- `result`: The returned data from the tool execution

---

### Agent Response Without Tool Calls

When agent responds without calling tools (e.g., clarification, error, context-based):

```json
{
  "sender": "agent",
  "content": "I'm not sure which company you're asking about. Could you provide the stock symbol (e.g., AAPL, MSFT)?",
  "timestamp": "2026-02-26T14:30:05Z",
  "tool_calls": []
}
```

**Note**: `tool_calls` is empty list (not null) when no tools were invoked.

---

## Session State Format

Data stored in Streamlit's `st.session_state`:

```python
st.session_state = {
    "selected_company": Company(symbol="AAPL", name="Apple Inc."),
    "stock_prices": [StockPrice(...), StockPrice(...), ...],
    "agent_session": <CopilotAgent instance>,
    "chat_history": [
        ChatMessage(...),  # User message
        ChatMessage(...),  # Agent response with tool_calls
        ChatMessage(...),  # User message
        ChatMessage(...)   # Agent response
    ]
}
```

**Initialization** (in app startup):
```python
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
if "selected_company" not in st.session_state:
    st.session_state.selected_company = COMPANIES[0]  # Default to first
    
if "stock_prices" not in st.session_state:
    st.session_state.stock_prices = []
    
if "agent_session" not in st.session_state:
    st.session_state.agent_session = initialize_agent()
```

---

## Agent Input Message Format

Message sent to Copilot SDK agent:

```python
{
    "user_message": "What is the average price?",
    "context": {
        "selected_company": {
            "symbol": "AAPL",
            "name": "Apple Inc."
        },
        "current_prices": [
            {"date": "2026-02-22", "open": 150.0, ...},
            ...
        ],
        "chat_history": [
            {"sender": "user", "content": "..."},
            {"sender": "agent", "content": "..."},
            ...
        ]
    }
}
```

**Purpose**: Provides agent with context about current UI state and previous conversation

**Format for Copilot SDK**:
```python
# In code:
response = agent.send_message(
    message=user_message,
    context={
        "company": st.session_state.selected_company,
        "prices": st.session_state.stock_prices,
        "history": st.session_state.chat_history
    }
)
```

---

## Agent Response Parsing

Response from Copilot SDK agent:

```python
{
    "message": "The average price is $151.96...",
    "tool_calls": [
        {
            "tool_name": "get_stock_data",
            "args": {"symbol": "AAPL"},
            "result": [...]
        }
    ],
    "model": "claude-haiku-4.5",
    "usage": {
        "input_tokens": 245,
        "output_tokens": 120
    }
}
```

**Parsing Logic** (in Streamlit app):
```python
response = agent.send_message(user_message)

# Extract message
agent_text = response.get("message", "")

# Extract tool calls
tool_calls = response.get("tool_calls", [])

# Create ChatMessage
chat_msg = ChatMessage(
    sender="agent",
    content=agent_text,
    timestamp=datetime.now(timezone.utc).isoformat(),
    tool_calls=tool_calls if tool_calls else None
)

# Add to history
st.session_state.chat_history.append(chat_msg)
```

---

## Error Response Format

When tool execution fails or agent encounters error:

```json
{
  "sender": "agent",
  "content": "I encountered an error while fetching data. Please try again.",
  "timestamp": "2026-02-26T14:30:05Z",
  "tool_calls": [
    {
      "name": "get_stock_data",
      "args": {
        "symbol": "INVALID"
      },
      "result": {
        "error": "Company symbol 'INVALID' not found. Available: AAPL, MSFT, GOOGL, AMZN, TSLA"
      }
    }
  ]
}
```

**Note**: Error details are included in tool_calls result for transparency

---

## Message Sequence Examples

### Example 1: Simple Price Query

```
User Input:
  "What is AAPL's average price?"

Agent Output:
{
  "sender": "agent",
  "content": "The average closing price of AAPL over the last 5 days is $151.96.",
  "timestamp": "2026-02-26T14:30:05Z",
  "tool_calls": [
    {
      "name": "get_stock_data",
      "args": {"symbol": "AAPL"},
      "result": [StockPrice data]
    }
  ]
}
```

### Example 2: Multi-Company Comparison (Agent calls tool twice)

```
User Input:
  "Which is more expensive, Apple or Google?"

Agent Output:
{
  "sender": "agent",
  "content": "Based on today's closing prices, Google ($2,850.30) is more expensive than Apple ($150.50). Google's stock is about 19x higher in price.",
  "timestamp": "2026-02-26T14:30:05Z",
  "tool_calls": [
    {
      "name": "get_stock_data",
      "args": {"symbol": "AAPL"},
      "result": [StockPrice data]
    },
    {
      "name": "get_stock_data",
      "args": {"symbol": "GOOGL"},
      "result": [StockPrice data]
    }
  ]
}
```

### Example 3: Follow-Up Question (Conversation Context Maintained)

```
First User:
  "What is MSFT's trend?"

Agent:
  (calls get_stock_data for MSFT, responds with trend analysis)

Second User:
  "Why did it go down?"

Agent Output:
{
  "sender": "agent",
  "content": "While I can see from the data that Microsoft's price decreased from $420.00 to $405.00 over the 5-day period, the actual reasons for price movements (market sentiment, earnings, economic factors, etc.) are not captured in historical price data. I only have access to the stock prices themselves.",
  "timestamp": "2026-02-26T14:30:15Z",
  "tool_calls": []  // No new tool calls needed - agent uses previous context
}
```

---

## Validation Rules

| Field | Rule | Example |
|-------|------|---------|
| sender | "user" or "agent" (string) | ✓ "user", ✗ "User" |
| content | 1-4096 chars, non-empty | ✓ "Tell me about Apple", ✗ "" |
| timestamp | ISO 8601 UTC | ✓ "2026-02-26T14:30:00Z", ✗ "Feb 26" |
| tool_calls | null (user msgs) or list (agent) | ✓ null, ✓ [], ✗ "none" |
| tool.name | String in ["get_stock_data", "analyze_stock_data"] | ✓ "get_stock_data" |
| tool.args | Dict with required keys | ✓ {"symbol": "AAPL"} |
| tool.result | Data or error dict | ✓ [StockPrice(...)] or {"error": "..."} |

---

## Notes

- All timestamps are UTC (Z suffix)
- Tool results are embedded in ChatMessage for display (shows what agent accessed)
- Long responses are not truncated in storage (but UI may truncate for display)
- No pagination needed (chat history is session-only, ~20-30 messages max)

