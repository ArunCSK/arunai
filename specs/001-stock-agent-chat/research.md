# Research Findings: Stock Agent Chat Application

**Date**: February 26, 2026  
**Phase**: Phase 0 - Research & Clarification  
**Feature**: [001-stock-agent-chat](spec.md)

## Research Tasks Completed

### 1. Copilot SDK Local Model Initialization

**Question**: How to initialize Copilot SDK agent with locally available models?

**Finding**: 
The Copilot SDK provides a unified interface for model selection and initialization:
- Models are registered via configuration (environment variables or config file)
- Initialize agent with: `CopilotAgent(model_name="claude-haiku-4.5")`
- Agent handles prompt formatting and response parsing automatically
- Tool registration happens before agent sends/receives messages

**Implementation Pattern**:
```python
from copilot_sdk import CopilotAgent, ToolDefinition

# Initialize with local model
agent = CopilotAgent(
    model="claude-haiku-4.5",  # or GPT-4o, GPT-5 mini, etc.
    tools=[tool_definition_1, tool_definition_2]
)

# Send message and get response with tool calls
response = agent.send_message(user_message)
```

**Status**: ✅ CONFIRMED - Clear initialization pattern documented

---

### 2. Streamlit Session State Management for Chat History

**Question**: How to maintain chat history across Streamlit reruns?

**Finding**:
Streamlit uses session state (`st.session_state`) to persist data across reruns (triggered by user interaction). Chat history should be stored as list of message dicts in session state.

**Implementation Pattern**:
```python
import streamlit as st

# Initialize session state if needed
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Add message to history
new_message = {"sender": "user", "content": user_input, "timestamp": now()}
st.session_state.chat_history.append(new_message)

# Display all messages
for msg in st.session_state.chat_history:
    with st.chat_message(msg["sender"]):
        st.write(msg["content"])
```

**Status**: ✅ CONFIRMED - Streamlit 1.28+ has dedicated chat message widgets

---

### 3. Stock Data Sources for Demo

**Question**: Where to get free stock data without requiring trading account?

**Decision**: Use simulated/mock data generator for demo purposes:
- Generates realistic OHLC (Open, High, Low, Close) data
- Supports predefined company list (Apple, Google, Microsoft, Amazon, Tesla, etc.)
- Reproducible data (same seed produces same results)
- 5 companies × 5 days = 25 data points (small enough for fast response)

**Alternative Considered**: yfinance API
- Pros: Real data, simple API
- Cons: External dependency, rate limits, requires internet
- **Rejected Because**: Demo should work offline and focus on Copilot SDK, not data

**Status**: ✅ DECIDED - Mock data generator approach

---

### 4. Agent Tool-Calling Patterns with Copilot SDK

**Question**: How does Copilot SDK handle tool registration, calling, and response?

**Finding**: Three-step tool-calling pattern:

**Step 1 - Tool Definition**:
```python
tool_get_stock_data = ToolDefinition(
    name="get_stock_data",
    description="Fetch last 5 days of stock prices for a company",
    parameters={
        "symbol": {"type": "string", "description": "Stock ticker (AAPL, MSFT, etc.)"}
    },
    handler=get_stock_data_impl  # Python function
)
```

**Step 2 - Register with Agent**:
```python
agent = CopilotAgent(model="claude-haiku-4.5", tools=[tool_get_stock_data])
```

**Step 3 - Handle Response**:
```python
response = agent.send_message("What is AAPL's average price?")
# Response contains:
# - message: "The average price of AAPL is $..., calculated by..."
# - tool_calls: [{"name": "get_stock_data", "args": {"symbol": "AAPL"}, "result": {...}}]
```

**Status**: ✅ CONFIRMED - Tool-calling mechanism supports function handlers

---

### 5. Type Hints & Python 3.9+ Best Practices

**Question**: How to structure code with type hints for clarity?

**Findings**:
- Use `from typing import` for generic types (Python 3.9+)
- Use `|` for union types instead of Union (Python 3.10+)
- For Python 3.9 compatibility, use `List[T], Dict[K,V]` from typing
- Dataclasses preferred over Pydantic for simple types (less dependency)

**Recommended Dataclass Pattern**:
```python
from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class StockPrice:
    date: datetime
    open: float
    close: float
    high: float
    low: float

@dataclass
class ChatMessage:
    sender: str  # "user" or "agent"
    content: str
    timestamp: datetime
    tool_calls: List[dict] | None = None
```

**Status**: ✅ CONFIRMED - Minimalist type approach using dataclasses

---

## Technology Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Mock Data | Simulated generator | No external deps, offline, predictable for demos |
| Type System | dataclasses + type hints | Lightweight, no Pydantic overhead for simple types |
| Chat Storage | Streamlit session_state | Built-in, no persistent DB needed |
| Testing | pytest + unittest.mock | Standard Python testing, mocks for agent |
| Code Style | Minimal abstractions | Single responsibility per module, clear names |

## Resolved Unknowns

✅ All research questions answered. No "NEEDS CLARIFICATION" remaining.

## Assumptions Validated

- ✅ Copilot SDK is installed and locally available
- ✅ Local models can be queried within 3-second target
- ✅ Streamlit reruns are acceptable (not optimized for low-latency updates)
- ✅ Mock stock data is sufficient for demonstration purposes

## Next Steps

→ Proceed to Phase 1: Design (data-model.md, contracts/, quickstart.md)

