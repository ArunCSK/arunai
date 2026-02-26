# Stock Analysis Tools - Developer Reference

This document explains the stock tools available to the Copilot Agent.

## Tool Functions

All tools return JSON strings for compatibility with the Copilot SDK.

### 1. `get_stock_price(symbol: str) -> str`

Get the current stock price and basic information.

**Parameters:**
- `symbol`: Stock ticker (e.g., "AAPL", "MSFT")

**Returns:**
```json
{
  "symbol": "AAPL",
  "current_price": 195.87,
  "currency": "USD",
  "timestamp": "2026-02-26T10:30:00"
}
```

**Example Usage:**
```python
result = get_stock_price("AAPL")
print(result)
# {"symbol": "AAPL", "current_price": 195.87, ...}
```

**When Agent Uses It:**
- "What's the current price of Apple?"
- "How much is MSFT trading at?"

---

### 2. `get_last_5_days_prices(symbol: str) -> str`

Retrieve OHLC (Open, High, Low, Close) data for the last 5 trading days.

**Parameters:**
- `symbol`: Stock ticker

**Returns:**
```json
{
  "symbol": "MSFT",
  "period": "Last 5 trading days",
  "prices": [
    {
      "date": "2026-02-20",
      "open": 397.50,
      "high": 399.25,
      "low": 395.75,
      "close": 397.23,
      "volume": 15234000
    },
    // 4 more days...
  ],
  "timestamp": "2026-02-26T10:30:00"
}
```

**Example Usage:**
```python
result = get_last_5_days_prices("MSFT")
data = json.loads(result)
for day in data["prices"]:
    print(f"{day['date']}: Close ${day['close']}")
```

**When Agent Uses It:**
- "Show me Microsoft's last 5 days of trading"
- "What are Apple's OHLC values for the past week?"

---

### 3. `get_stock_comparison(symbol1: str, symbol2: str) -> str`

Compare two stocks over the last 5 trading days.

**Parameters:**
- `symbol1`: First stock ticker
- `symbol2`: Second stock ticker

**Returns:**
```json
{
  "symbol1": "AAPL",
  "symbol2": "MSFT",
  "last_close_1": 195.87,
  "last_close_2": 397.23,
  "5day_change_1": 2.15,
  "5day_change_2": -1.50
}
```

**Example Usage:**
```python
result = get_stock_comparison("AAPL", "MSFT")
data = json.loads(result)
print(f"AAPL changed {data['5day_change_1']}%")
print(f"MSFT changed {data['5day_change_2']}%")
```

**When Agent Uses It:**
- "Compare Apple and Microsoft"
- "Which performed better, Tesla or Nvidia?"

---

### 4. `get_available_stocks() -> str`

Get a list of popular stocks organized by category.

**Parameters:**
- None

**Returns:**
```json
{
  "Technology": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META"],
  "Finance": ["JPM", "BAC", "WFC", "GS", "MS"],
  "Healthcare": ["JNJ", "UNH", "PFE", "ABBV", "TMO"],
  "Industry": ["CAT", "MMM", "BA", "GE"],
  "Other": ["NKE", "MCD", "KO", "PG", "WMT"]
}
```

**Example Usage:**
```python
result = get_available_stocks()
stocks = json.loads(result)
for category, symbols in stocks.items():
    print(f"{category}: {', '.join(symbols)}")
```

**When Agent Uses It:**
- "What stocks are available?"
- "Show me some popular tech stocks"

---

### 5. `analyze_stock_trend(symbol: str) -> str`

Analyze the price trend over the last 5 trading days.

**Parameters:**
- `symbol`: Stock ticker

**Returns:**
```json
{
  "symbol": "GOOGL",
  "trend": "DOWNTREND",
  "5day_change_percent": -2.41,
  "high_5day": 198.75,
  "low_5day": 192.50,
  "starting_price": 197.65,
  "ending_price": 192.88
}
```

**Trend Categories:**
- `UPTREND`: Change > +2%
- `DOWNTREND`: Change < -2%
- `STABLE`: Change between -2% and +2%

**Example Usage:**
```python
result = analyze_stock_trend("GOOGL")
data = json.loads(result)
print(f"Trend: {data['trend']}")
print(f"5-day change: {data['5day_change_percent']}%")
```

**When Agent Uses It:**
- "Is Apple going up or down?"
- "What's the trend for Tesla?"

---

## Adding Custom Tools

To add a new tool, follow this pattern:

```python
from typing import Annotated
import json

def my_new_tool(
    param1: Annotated[str, "Description of param1"],
    param2: Annotated[int, "Description of param2"],
) -> str:
    """
    Tool description shown to the agent.
    Be clear and descriptive!
    """
    try:
        # Your implementation
        result = {"success": True, "data": "..."}
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})
```

**Key Requirements:**
1. Use `Annotated` for parameter descriptions
2. Include docstring for tool description
3. Always return JSON string
4. Handle errors gracefully
5. Register in `agent.py` `tools` list

## Tool Best Practices

### 1. **Always Error Check**
```python
if data.empty:
    return json.dumps({"error": "No data found"})
```

### 2. **Format Numbers Consistently**
```python
return json.dumps({"price": round(float(value), 2)})
```

### 3. **Include Timestamps**
```python
"timestamp": datetime.now().isoformat()
```

### 4. **Provide Context**
```python
return json.dumps({
    "symbol": symbol.upper(),  # Always uppercase symbols
    "period": "Last 5 trading days",
    "data": prices
})
```

### 5. **Use Meaningful Keys**
```python
# Good
{"closing_price": 100.50}

# Bad
{"cp": 100.50}
```

## Integration with Agent

Tools are registered in `agent.py`:

```python
self.agent = ChatAgent(
    chat_client=self.chat_client,
    instructions="You are a helpful stock analysis assistant...",
    tools=[
        get_stock_price,
        get_last_5_days_prices,
        get_stock_comparison,
        get_available_stocks,
        analyze_stock_trend,
        # Add your custom tools here
    ]
)
```

## Testing Tools Independently

Test tools without running the agent:

```python
# test_tools.py
from agent_tools import get_stock_price
import json

result = get_stock_price("AAPL")
data = json.loads(result)
print(data)
```

Run:
```bash
python test_tools.py
```

## Performance Considerations

### Data Fetching
- yfinance caches data automatically
- First call takes longer (~0.5s)
- Subsequent calls are faster (~0.1s)

### Tool Selection
- Use specific tools when possible
- `get_last_5_days_prices()` is cheaper than looping `get_stock_price()`
- Avoid redundant calls in one conversation

### Agent Efficiency
- Clear, specific instructions help agent choose right tool
- Longer context = slower responses
- Consider tool combining (e.g., comparison includes trend info)

## Error Handling Examples

### Missing Symbol
```python
try:
    stock = yf.Ticker(symbol.upper())
    data = stock.history(period="1d")
    if data.empty:
        return json.dumps({"error": f"Stock symbol {symbol} not found"})
except Exception as e:
    return json.dumps({"error": str(e)})
```

### API Rate Limits
```python
import time

def get_stock_with_retry(symbol: str, retries: int = 3) -> str:
    for attempt in range(retries):
        try:
            return get_stock_price(symbol)
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1)  # Wait before retry
            else:
                return json.dumps({"error": f"Failed after {retries} attempts"})
```

## Future Tool Ideas

1. **News Integration**
   ```python
   def get_stock_news(symbol: str) -> str:
       # Get latest news articles
   ```

2. **Technical Analysis**
   ```python
   def calculate_moving_average(symbol: str, days: int) -> str:
       # Calculate MA
   ```

3. **Portfolio Analysis**
   ```python
   def analyze_portfolio(symbols: List[str]) -> str:
       # Portfolio metrics
   ```

4. **Earnings Data**
   ```python
   def get_earnings_info(symbol: str) -> str:
       # Earnings dates and estimates
   ```

5. **Dividend Information**
   ```python
   def get_dividend_info(symbol: str) -> str:
       # Dividend yields and dates
   ```

---

**Remember**: The agent will describe tools to the user automatically, so write clear descriptions and keep tools focused and single-purpose!
