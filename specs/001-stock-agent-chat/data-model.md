# Data Model: Stock Agent Chat Application

**Phase**: Phase 1 - Design  
**Date**: February 26, 2026  
**Feature**: [001-stock-agent-chat](spec.md)

## Core Data Models

All models use Python dataclasses for simplicity and type safety.

### StockPrice

Represents a single day's stock price data (OHLC format).

```python
@dataclass
class StockPrice:
    date: str              # ISO format: "2026-02-26"
    open: float            # Opening price
    close: float           # Closing price
    high: float            # Daily high
    low: float             # Daily low
```

**Constraints**:
- All prices are positive floats (dollars)
- Date format is ISO 8601 (YYYY-MM-DD)
- Data is read-only (no updates after creation)

**Example**:
```python
StockPrice(
    date="2026-02-26",
    open=150.25,
    close=152.80,
    high=153.50,
    low=149.75
)
```

### Company

Represents a publicly traded company that the app supports.

```python
@dataclass
class Company:
    symbol: str            # Ticker symbol (e.g., "AAPL")
    name: str              # Full company name (e.g., "Apple Inc.")
```

**Constraints**:
- Symbol is uppercase 1-5 characters
- Name is human-readable display text
- Immutable (no changes after creation)

**Example**:
```python
Company(symbol="AAPL", name="Apple Inc.")
```

### ChatMessage

Represents a single message in the chat conversation.

```python
@dataclass
class ChatMessage:
    sender: str                              # "user" or "agent"
    content: str                             # Message text
    timestamp: str                           # ISO timestamp
    tool_calls: list[dict] | None = None    # Agent tool invocations (if any)
```

**Constraints**:
- sender must be "user" or "agent"
- content is non-empty text
- timestamp is ISO 8601 format
- tool_calls is list of dicts with keys: {name, args, result}

**Example (User Message)**:
```python
ChatMessage(
    sender="user",
    content="What is the average price?",
    timestamp="2026-02-26T14:30:00Z",
    tool_calls=None
)
```

**Example (Agent Message with Tool Info)**:
```python
ChatMessage(
    sender="agent",
    content="The average price of AAPL over 5 days is $151.50, calculated from open/close prices.",
    timestamp="2026-02-26T14:30:05Z",
    tool_calls=[
        {
            "name": "get_stock_data",
            "args": {"symbol": "AAPL"},
            "result": [StockPrice(...), StockPrice(...), ...]
        }
    ]
)
```

### ToolResult

Represents the result of a tool execution by the agent.

```python
@dataclass
class ToolResult:
    name: str              # Tool name (e.g., "get_stock_data")
    success: bool          # True if tool executed successfully
    data: dict | list      # Tool output data
    error: str | None      # Error message if success=False
```

**Example (Success)**:
```python
ToolResult(
    name="get_stock_data",
    success=True,
    data=[StockPrice(...), StockPrice(...), ...],
    error=None
)
```

**Example (Failure)**:
```python
ToolResult(
    name="get_stock_data",
    success=False,
    data={},
    error="Company symbol 'INVALID' not found"
)
```

## Data Flow Diagrams

### Stock Data Selection Flow

```
User selects company from dropdown
    ↓
Streamlit reruns with selected company
    ↓
stock_data.get_stock_prices(symbol) → StockPrice[]
    ↓
Display prices in st.dataframe()
    ↓
Agent has access to prices via chat context
```

### Chat Message Flow

```
User types message
    ↓
User clicks Submit
    ↓
Message added to session_state.chat_history
    ↓
agent.send_message(user_message, context=current_prices) → response
    ↓
Response parsed (extract message + tool_calls)
    ↓
ChatMessage(sender="agent", content=msg, tool_calls=calls) added to history
    ↓
UI rerenders chat history with new messages
```

### Agent Tool-Calling Flow

```
Agent receives: "What is AAPL's average price?"
    ↓
Agent analyzes: Needs stock data → call get_stock_data tool
    ↓
Copilot SDK calls tool handler with args: {symbol: "AAPL"}
    ↓
get_stock_data_impl() fetches 5 days of prices
    ↓
Copilot SDK passes result back to agent
    ↓
Agent generates response using tool result
    ↓
Response: "AAPL's average price is $151.50..." + tool_calls metadata
```

## Validation Rules

### StockPrice Validation
- date matches ISO 8601 format
- All prices (open, close, high, low) > 0
- high >= max(open, close)
- low <= min(open, close)

### Company Validation
- symbol is 1-5 uppercase letters/digits
- name is non-empty string

### ChatMessage Validation
- sender is "user" or "agent"
- content is non-empty string (max 4096 chars)
- timestamp matches ISO 8601
- tool_calls (if present) is list of dicts with {name, args, result}

## Storage & Persistence

**In-Memory During Session**:
- Chat history: `st.session_state["chat_history"]` → list[ChatMessage]
- Current company: `st.session_state["selected_company"]` → Company
- Current stock prices: `st.session_state["stock_prices"]` → list[StockPrice]

**No Persistence**: Data is ephemeral (clears on app restart)

**Rationale**: Demo application only. Users re-run to see fresh results.

## Relationships

```
Company
  └─ StockPrice[] (1-to-many: one company has multiple days of prices)
      
ChatMessage[] (conversation history)
  └─ Tool results can reference StockPrice[] data
     
Agent
  └─ Uses StockPrice[] from context
  └─ Calls tools that return StockPrice[] or analysis
```

## Type Summary

| Model | Source | Scope | Lifecycle |
|-------|--------|-------|-----------|
| Company | Hardcoded list | Global | Immutable |
| StockPrice | Generated/API | Per session | Memory only |
| ChatMessage | User + Agent | Per session | Session state |
| ToolResult | Tool execution | Tool call | Embedded in ChatMessage |

## Next Step

→ Proceed to Phase 1 Design Contracts: `contracts/`
