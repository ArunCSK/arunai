# Tool Contracts: Stock Agent Chat Application

**Phase**: Phase 1 - Design  
**Date**: February 26, 2026  
**Feature**: [001-stock-agent-chat](../spec.md)

## Tool 1: get_stock_data

**Purpose**: Retrieve stock price data for a given company.

**Tool Registration Schema**:
```json
{
  "name": "get_stock_data",
  "description": "Fetch the last 5 days of stock price data (OHLC) for a company by ticker symbol",
  "parameters": {
    "type": "object",
    "properties": {
      "symbol": {
        "type": "string",
        "description": "Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)"
      }
    },
    "required": ["symbol"]
  }
}
```

**Input Contract**:
```python
symbol: str  # Uppercase, 1-5 chars (e.g., "AAPL")
```

**Output Contract** (Success):
```python
# Returns list of StockPrice objects
[
    {"date": "2026-02-22", "open": 150.0, "close": 151.5, "high": 152.0, "low": 149.5},
    {"date": "2026-02-23", "open": 151.5, "close": 152.8, "high": 153.5, "low": 151.0},
    {"date": "2026-02-24", "open": 152.8, "close": 153.2, "high": 154.0, "low": 152.5},
    {"date": "2026-02-25", "open": 153.2, "close": 151.8, "high": 154.2, "low": 151.5},
    {"date": "2026-02-26", "open": 151.8, "close": 150.5, "high": 152.0, "low": 150.0}
]
```

**Output Contract** (Failure):
```python
{
    "error": "Company symbol 'INVALID' not found. Available symbols: AAPL, MSFT, GOOGL, AMZN, TSLA"
}
```

**Error Cases**:
- Symbol not found: Return error message with list of valid symbols
- Empty symbol: Return error
- Symbol length > 5: Return error

**Validation**:
- Symbol is non-empty string
- Returns exactly 5 days of data (or error if not available)
- All prices are positive numbers
- High >= Open/Close, Low <= Open/Close

---

## Tool 2: analyze_stock_data

**Purpose**: Perform analysis on stock prices to answer user questions.

**Tool Registration Schema**:
```json
{
  "name": "analyze_stock_data",
  "description": "Analyze stock price data to answer questions about trends, averages, highs, lows, etc.",
  "parameters": {
    "type": "object",
    "properties": {
      "symbol": {
        "type": "string",
        "description": "Stock ticker symbol"
      },
      "question": {
        "type": "string",
        "description": "The analysis question to answer (e.g., 'What is the average price?', 'Did price go up?')"
      }
    },
    "required": ["symbol", "question"]
  }
}
```

**Input Contract**:
```python
symbol: str       # Uppercase, 1-5 chars
question: str     # Natural language analysis question
```

**Output Contract** (Success):
```python
# Returns analysis result as JSON
{
    "symbol": "AAPL",
    "question": "What is the average price?",
    "answer": "The average closing price over 5 days is $152.00",
    "reasoning": "Calculated from closing prices: (151.5 + 152.8 + 153.2 + 151.8 + 150.5) / 5 = $151.96"
}
```

**Special Cases**:
```python
# Trend analysis
{
    "symbol": "AAPL",
    "question": "Did the price go up?",
    "answer": "No, the price decreased from $151.50 to $150.50 (down 0.65%)",
    "reasoning": "First day close: $151.50, Last day close: $150.50"
}

# High/Low analysis  
{
    "symbol": "AAPL",
    "question": "What was the highest price?",
    "answer": "The highest price was $154.20 on 2026-02-25",
    "reasoning": "Found max high across all days"
}
```

**Error Cases**:
```python
{
    "error": "Could not analyze: [reason]",
    "symbol": "INVALID",
    "question": "What is the average?"
}
```

**Validation**:
- Symbol must be valid (exists in company list)
- Question is non-empty string
- Answer addresses the question (agent responsible for semantic correctness)

---

## Tool Calling Expectations

### Tool Calling Sequence

The Copilot SDK agent will invoke tools based on user questions:

```
User: "What is the average price of AAPL?"
  ↓
Agent decides: Needs stock data
  ↓
Agent calls: get_stock_data(symbol="AAPL")
  ↓
Agent receives: [StockPrice[], StockPrice[], ...]
  ↓
Agent generates response: "The average price is $151.96, calculated from..."
```

### Multi-Tool Sequences

For complex questions, agent may call multiple tools:

```
User: "Is Google's price higher or lower than Microsoft's?"
  ↓
Agent decides: Need both prices
  ↓
Agent calls: get_stock_data(symbol="GOOGL")
Agent calls: get_stock_data(symbol="MSFT")
  ↓
Agent compares and responds
```

### Tool Response in Chat Context

After tool execution, the agent receives:
```python
{
    "tool_name": "get_stock_data",
    "args": {"symbol": "AAPL"},
    "result": [StockPrice(...), ...],
    "timestamp": "2026-02-26T14:30:00Z"
}
```

The agent uses this metadata to generate a response that explains which tools were used.

---

## Tool Implementation Notes

### get_stock_data Handler
- Takes symbol string
- Fetches from mock data generator (same data each session)
- Validates symbol against known companies
- Returns StockPrice list or error dict

### analyze_stock_data Handler
- Takes symbol and question
- Retrieves prices for symbol (calls get_stock_data internally)
- Parses question type (trend, average, high/low, etc.)
- Generates analysis JSON
- Returns analysis result

---

## Parameter Validation & Edge Cases

| Parameter | Valid | Invalid | Behavior |
|-----------|-------|---------|----------|
| symbol | "AAPL", "MSFT" | "invalid", "aapl" (lowercase) | Return error message with valid list |
| question | "What is the average?" | Empty string | Return error: question required |
| price values | 150.25, 0.01 | -100, NaN | Validation fails (reject malformed data) |

---

## Success Criteria for Tools

- ✅ Tool registered with Copilot SDK
- ✅ Tool callable by agent without user intervention
- ✅ Tool returns data in documented format
- ✅ Tool errors handled gracefully (error dict, not exception)
- ✅ Agent successfully uses tool results in response
- ✅ Tool result visible in chat (shows which tools were called)

