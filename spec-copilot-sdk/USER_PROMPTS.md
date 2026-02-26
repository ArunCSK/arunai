# User Prompts for Copilot Agent Tool Analysis

This guide shows example user prompts that trigger the agent to call tools for stock analysis.

---

## 📈 Get Stock Data Tool

Use these prompts to retrieve raw OHLC (Open, High, Low, Close) price data.

### Prompt Examples:

```
"Show me the stock prices for Apple"
"What are the last 5 days of Microsoft prices?"
"Get GOOGL data"
"Display Amazon stock data"
"Can I see Tesla's prices?"
"What were the prices for MSFT?"
"Show AAPL prices for the last 5 days"
"Get the historical data for Tesla"
```

### Agent Response:
- Calls: `get_stock_data(symbol="AAPL")`
- Returns: 5 days of OHLC data in a formatted table

---

## 📊 Analyze Stock Data Tool

### Average Price Analysis

Use these prompts to get average/mean closing prices.

```
"What is the average price of Apple?"
"What's the mean closing price for MSFT?"
"Calculate the typical price for Google stock"
"What's the average for AMZN?"
"Tell me the mean price of Tesla"
"What's the typical closing price for Microsoft?"
"Average price for AAPL?"
```

**Tool Call**: `analyze_stock_data(symbol="AAPL", question="average")`

**Agent Response**:
```
The average closing price over 5 days is $150.25
├─ Prices: [150.10, 151.20, 150.25, 152.10, 149.90]
└─ Average: $150.25
```

---

### Trend Analysis

Use these prompts to analyze price direction (up/down) and percentage change.

```
"Is Apple trending up or down?"
"Did Microsoft prices increase?"
"Is Google going up?"
"What's the trend for Amazon stock?"
"Did Tesla go up?"
"How did MSFT perform over the 5 days?"
"Is the price increasing or decreasing for AAPL?"
"Did GOOGL prices rise?"
"Show me the trend for AMZN"
"Is TSLA going down?"
```

**Tool Call**: `analyze_stock_data(symbol="AAPL", question="Is it trending up?")`

**Agent Response**:
```
The price went up from $150.25 to $152.10 (+1.23%)
├─ Start Price: $150.25
├─ End Price: $152.10
└─ Change: +$1.85 (+1.23%)
```

---

### High/Low Analysis

Use these prompts to find the highest and lowest prices.

```
"What was the highest price for Apple?"
"What's the lowest point for Microsoft?"
"Show me the high and low for Google"
"When did Amazon reach its peak?"
"What was the bottom price for Tesla?"
"Maximum and minimum for AAPL?"
"What's the peak price for MSFT?"
"Find the lowest price for GOOGL"
"High and low for AMZN?"
"What was the maximum price for TSLA?"
```

**Tool Call**: `analyze_stock_data(symbol="AAPL", question="What's the highest and lowest?")`

**Agent Response**:
```
Highest: $153.50 on 2026-02-20, Lowest: $149.90 on 2026-02-19
├─ Highest Price: $153.50 (Feb 20)
└─ Lowest Price: $149.90 (Feb 19)
```

---

### Volatility Analysis

Use these prompts to understand price swings and volatility.

```
"What's the volatility for Apple?"
"How volatile is Microsoft stock?"
"Is Google stock stable or volatile?"
"What's the price range for Amazon?"
"How much does Tesla swing daily?"
"Show volatility for AAPL"
"Is MSFT stable?"
"What's the daily swing for GOOGL?"
"How much variation for AMZN?"
"Price volatility for TSLA?"
```

**Tool Call**: `analyze_stock_data(symbol="AAPL", question="volatility")`

**Agent Response**:
```
Average daily range: $2.15, Max range: $3.50
├─ Volatility Level: Moderate
├─ Average Daily Range: $2.15
└─ Max Daily Range: $3.50
```

---

## 🔗 Multi-Turn Conversation Examples

The agent maintains context across multiple messages:

### Example 1: Start with Data, Then Analyze
```
User: "Show me Apple stock data"
Agent: [Displays 5 days of AAPL prices]

User: "What's the average?"
Agent: [Uses get_stock_data result from context]
        → The average closing price is $150.25

User: "Is it trending up?"
Agent: [Uses context]
        → The price went up from $150.25 to $152.10 (+1.23%)
```

### Example 2: Sequential Analysis Questions
```
User: "Get Tesla data"
Agent: [Calls get_stock_data for TSLA]

User: "What's the volatility?"
Agent: [Calls analyze_stock_data for volatility]

User: "When was the peak?"
Agent: [Calls analyze_stock_data for high/low]

User: "Compare it to Microsoft"
Agent: [Switches context to MSFT, performs analysis]
```

### Example 3: Complex Analysis
```
User: "Which company is most stable - Apple or Google?"
Agent: 
  → Calls analyze_stock_data(AAPL, volatility)
  → Calls analyze_stock_data(GOOGL, volatility)
  → Compares volatility levels

User: "Show me their trends"
Agent:
  → Calls analyze_stock_data(AAPL, trend)
  → Calls analyze_stock_data(GOOGL, trend)
  → Shows comparison
```

---

## 💡 Pro Tips for Best Results

### ✅ Good Prompts (Specific)
```
"What's the average price of MSFT?"
"Is Google trending up?"
"Show volatility for Tesla"
"When did Apple reach its highest point?"
```

### ❌ Vague Prompts (Still Work, But Less Specific)
```
"Tell me about Apple"
"How's Microsoft doing?"
"What about Google?"
→ Falls back to summary statistics
```

### 🔄 Context-Aware
The agent remembers which company you selected and uses it for subsequent questions:
```
User: "Select Microsoft"
[UI: Company changed to MSFT]

User: "What's the average?"
Agent: [Automatically analyzes MSFT, not default]
```

---

## 📋 Tool Call Flow Diagram

```
User Input
    ↓
[Message Analyzer]
    ↓
┌─────────────────────────────────────────┐
│ Keyword Matching                        │
├─────────────────────────────────────────┤
│ Contains: price/data/show               │
│ → get_stock_data()                      │
│                                         │
│ Contains: average/mean/typical          │
│ → analyze_stock_data(...average...)     │
│                                         │
│ Contains: trend/up/down/increase        │
│ → analyze_stock_data(...trend...)       │
│                                         │
│ Contains: high/low/peak/bottom          │
│ → analyze_stock_data(...high_low...)    │
│                                         │
│ Contains: volatility/volatile/range     │
│ → analyze_stock_data(...volatility...)  │
│                                         │
│ Other                                   │
│ → analyze_stock_data(...summary...)     │
└─────────────────────────────────────────┘
    ↓
Tool Execution
    ↓
Response Formatting
    ↓
User Display
```

---

## 🎯 Expected Behavior by Prompt Type

| User Question | Tool Called | Analysis Type | Response Time |
|---|---|---|---|
| "Show Apple prices" | `get_stock_data` | Retrieval | <50ms |
| "Average price?" | `analyze_stock_data` | Average | <100ms |
| "Trending up?" | `analyze_stock_data` | Trend | <100ms |
| "High/low?" | `analyze_stock_data` | High/Low | <100ms |
| "How volatile?" | `analyze_stock_data` | Volatility | <100ms |
| "Tell me about it" | `analyze_stock_data` | Summary | <100ms |

---

## 🚀 Try These Combinations

### Beginner
1. "Show me Apple stock data"
2. "What's the average price?"

### Intermediate
1. "Get Microsoft prices"
2. "Is it trending up?"
3. "What's the volatility?"

### Advanced
1. "Get Google data"
2. "Analyze the trend"
3. "Is it more volatile than Amazon?"
4. "When was the peak?"

---

## 📝 Transcript Example

```
USER: "Hi! Can you help with stock analysis?"
AGENT: "Of course! I can help analyze stock prices for Apple, Microsoft, 
        Google, Amazon, or Tesla. What would you like to know?"

USER: "Show me Apple data"
AGENT: ✅ Called: get_stock_data(symbol="AAPL")
       Displaying 5 days of Apple stock prices...
       [Table with OHLC data]

USER: "What's the average?"
AGENT: ✅ Called: analyze_stock_data(symbol="AAPL", question="average")
       The average closing price over 5 days is $150.25

USER: "Is it trending up?"
AGENT: ✅ Called: analyze_stock_data(symbol="AAPL", question="trending up?")
       The price went up from $150.25 to $152.10 (+1.23%)

USER: "How volatile is it?"
AGENT: ✅ Called: analyze_stock_data(symbol="AAPL", question="volatility?")
       Average daily range: $2.15, Max range: $3.50
       Volatility level: Moderate

USER: "Compare it to Microsoft"
AGENT: ✅ Called: analyze_stock_data(symbol="MSFT", question="volatility?")
       Average daily range: $1.85, Max range: $3.20
       Volatility level: Moderate
       
       Both stocks show similar volatility patterns, but Microsoft has 
       slightly tighter daily ranges.
```

---

## Summary

The Copilot Agent understands **natural language** and automatically calls the right tools:
- 🎯 **Specific prompts** → More precise analysis
- 📊 **Multi-turn conversations** → Context-aware responses
- 🔄 **Context switching** → Changes focus to different stocks smoothly

Try the app with these prompts to see the agent in action!
