# Stock Analysis Dashboard with Copilot SDK

A minimalist web application demonstrating the Copilot SDK (Microsoft Agent Framework) with a practical use case: interactive stock analysis and price tracking.

## Features

✨ **What's Included:**
- 📈 **Stock Price Viewer** - Display last 5 trading days OHLC data with interactive charts
- 💬 **AI Assistant** - Copilot-powered agent that answers stock questions and provides analysis
- 🛠️ **Reusable Tools** - Pre-built functions for:
  - Getting current stock prices
  - Fetching 5-day historical data
  - Comparing two stocks
  - Analyzing price trends
  - Listing popular stocks
- 🎨 **Clean UI** - Built with Streamlit for a professional web interface
- 🔄 **Multi-turn Chat** - Maintain conversation context across multiple queries
- 🏃 **No Enterprise Setup** - Works locally without complex infrastructure

## Project Structure

```
copilot-sdk/
├── app.py                 # Main Streamlit application
├── agent.py               # Copilot SDK agent setup
├── agent_tools.py         # Reusable stock data tools
├── requirements.txt       # Python dependencies
├── .env                   # Configuration file
└── README.md             # This file
```

## Setup Instructions

### 1. **Install Dependencies**

The Python environment is pre-configured. Just install the packages:

```bash
# Navigate to project directory
cd c:\Users\Arun\projects\arunai\copilot-sdk

# Install all dependencies
pip install -r requirements.txt
```

### 2. **Configure API Access**

The agent needs an LLM to function. Choose one of these options:

#### Option A: OpenAI (Free Tier)
1. Get your free API key from: https://platform.openai.com/api-keys
2. Copy the key and set it in `.env`:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```
3. Free tier models available:
   - `gpt-4o-mini` (Recommended - fast and cheap)
   - `gpt-3.5-turbo` (Older, still powerful)

#### Option B: Azure OpenAI
1. Set up Azure OpenAI endpoint
2. Update `.env` with your credentials:
   ```
   AZURE_OPENAI_KEY=your-key
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_DEPLOYMENT=your-deployment-name
   ```

#### Option C: Local Model (Advanced)
For completely local inference without API keys:
1. Set up Ollama or similar local LLM
2. Modify `agent.py` to use local client instead of OpenAI

### 3. **Run the Application**

```bash
# From project directory, run Streamlit app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## How It Works

### Architecture

```
┌─────────────────────────────────────┐
│     Streamlit Web UI (Port 8501)    │
├─────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────┐ │
│  │  Stock Viewer    │  │   Chat   │ │
│  │  (5-Day Chart)   │  │ Interface│ │
│  └────────┬─────────┘  └────┬─────┘ │
│           │                 │       │
│           └─────────────────┘       │
└─────────────────┬───────────────────┘
                  │
        ┌─────────▼──────────┐
        │  Copilot SDK Agent │
        │ (Chat Agent w/ AI) │
        └─────────┬──────────┘
                  │
        ┌─────────▼──────────────────────┐
        │  Stock Analysis Tools      │
        │ - get_stock_price()            │
        │ - get_last_5_days_prices()     │
        │ - compare_stocks()             │
        │ - analyze_trend()              │
        │ - list_popular_stocks()        │
        └─────────┬──────────────────────┘
                  │
        ┌─────────▼──────────┐
        │    yfinance API    │
        │  (Free Stock Data) │
        └────────────────────┘
```

### Key Components

**1. Agent Tools** (`agent_tools.py`)
- Pure Python functions that fetch real-time stock data
- Used by the Copilot agent to answer questions
- Can be extended with more financial tools

**2. Copilot Agent** (`agent.py`)
- `StockAnalysisAgent` class wraps the Copilot SDK
- Manages agent lifecycle and multi-turn conversations
- Maintains context across multiple queries
- Automatically calls appropriate tools based on user questions

**3. Streamlit App** (`app.py`)
- Two-column layout:
  - **Left**: Stock price viewer with 5-day chart
  - **Right**: Chat interface powered by agent
- Real-time data updates
- Session management for conversation history

## Usage Examples

### Stock Price Lookup
**User**: "What's the current price of Apple?"
**Agent**: Calls `get_stock_price()` and returns the current price

### 5-Day Analysis
**User**: "Show me Microsoft's 5-day trend"
**Agent**: Calls `get_last_5_days_prices()` and analyzes the data

### Stock Comparison
**User**: "Compare Apple and Microsoft"
**Agent**: Calls `get_stock_comparison()` and provides analysis

### Trend Analysis
**User**: "Is Tesla going up or down?"
**Agent**: Calls `analyze_stock_trend()` and explains the direction

## File Details

### `agent_tools.py` - Reusable Tool Functions

These functions are available to the AI agent:

```python
# Get current price and info
get_stock_price(symbol: str) -> str

# Get 5 days of OHLC data
get_last_5_days_prices(symbol: str) -> str

# Compare two stocks
get_stock_comparison(symbol1: str, symbol2: str) -> str

# Get popular stock list
get_available_stocks() -> str

# Analyze price trend
analyze_stock_trend(symbol: str) -> str
```

### `agent.py` - Agent Setup

`StockAnalysisAgent` class handles:
- Initializing the Copilot SDK ChatAgent
- Registering tools for the agent
- Managing conversations with threading
- Cleanup and resource management

### `app.py` - UI

Streamlit app with:
- Stock dropdown selector
- Interactive price chart (Plotly)
- OHLC statistics table
- Chat message history
- VS Code-like chat styling

## Customization

### Add More Stock Tools
Edit `agent_tools.py` and add new functions following the pattern:
```python
def my_stock_function(
    param: Annotated[str, "Description"],
) -> str:
    """Tool description shown to agent."""
    # Implementation...
    return json.dumps({"result": data})
```

Then register in `agent.py`:
```python
tools=[
    get_stock_price,
    my_stock_function,  # Add here
    # ... other tools
]
```

### Change the Model
In `.env`, you can switch models:
```
# Faster, cheaper (Recommended)
gpt-4o-mini

# More capable
gpt-4-turbo

# Budget option
gpt-3.5-turbo
```

Or modify `agent.py` to use different providers (Anthropic, Google, Azure, etc.)

### Extend the UI
Streamlit is highly customizable:
- Add sidebar options for filtering stocks
- Add more charts and visualizations
- Integrate real-time notifications
- Add portfolio tracking

## Troubleshooting

### "OPENAI_API_KEY not set"
- Make sure your `.env` file has the correct key
- Streamlit doesn't automatically load `.env` - restart the app after changing it
- Check that your API key hasn't expired

### Agent not responding
- Check network connectivity
- Verify your API key is valid
- Look at the terminal output for detailed error messages
- Ensure you have API quota remaining

### Stock data not loading
- `yfinance` requires internet connection
- Some markets may be closed (check market hours)
- Try a different stock symbol if one fails

### Chat history grows too large
- Use "Clear Chat History" button to reset
- Each message is stored in Streamlit session state

## Performance Notes

- **Initial startup**: ~3-5 seconds (agent initialization)
- **Stock data fetch**: ~0.5-1 second per request (cached for same session)
- **Agent response**: 2-10 seconds (depends on API latency and complexity)
- **Chart rendering**: Instant (Plotly client-side)

## Security

⚠️ **Important**: Never commit `.env` with real API keys to version control
- `.env` should be in `.gitignore`
- Treat API keys like passwords
- Use GitHub Secrets for CI/CD

## Limits and Fair Use

**OpenAI Free Tier:**
- Limited requests and tokens
- Not recommended for production
- Perfect for learning and demos

**For Production:**
- Move to paid tier or Azure OpenAI
- Consider implementing caching
- Add rate limiting
- Use streaming responses

## Architecture Benefits

This architecture demonstrates:
- ✅ **Tool-augmented agents** - AI with real tool access
- ✅ **Context preservation** - Multi-turn conversations
- ✅ **Type-safe tools** - Python types guide the agent
- ✅ **Async/await** - Non-blocking operations
- ✅ **Clean separation** - Tools, agent, UI are independent
- ✅ **Minimal overhead** - ~100 lines of agent code
- ✅ **Extensible** - Easy to add more tools

## Next Steps

To enhance this application:

1. **Add more tools**: Options pricing, portfolio analysis, news integration
2. **Add persistence**: Save chat history to database
3. **Add authentication**: Multi-user support
4. **Add real-time updates**: WebSocket for live prices
5. **Deploy to cloud**: Streamlit Cloud, Azure, or AWS
6. **Add metrics**: Track agent accuracy and response times
7. **Multi-agent workflows**: Coordinator agent with specialist agents

## Resources

- **Copilot SDK**: https://github.com/microsoft/agent-framework
- **Streamlit**: https://streamlit.io/
- **yfinance**: https://github.com/ranaroussi/yfinance
- **Plotly**: https://plotly.com/python/
- **OpenAI API**: https://platform.openai.com/

## License

This project is provided as-is for educational and demonstration purposes.

---

**Made with ❤️ for the Copilot SDK Community**
