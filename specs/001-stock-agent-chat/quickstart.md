# Quick Start: Stock Agent Chat Application

**Phase**: Phase 1 - Design  
**Date**: February 26, 2026  
**Feature**: [001-stock-agent-chat](spec.md)

## For Developers: Quick Setup & Run

### Prerequisites

- Python 3.9 or higher
- Copilot SDK installed and configured locally
- One or more local LLM models available:
  - Claude Haiku 4.5 (preferred for speed)
  - GPT-4o
  - GPT-5 mini
  - Other supported models

### Installation

```bash
# Clone repository
git clone <repo-url>
cd spec-copilot-sdk

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify Copilot SDK installation
python -c "from copilot_sdk import CopilotAgent; print('Copilot SDK ready')"
```

### Running the Application

```bash
# Start the Streamlit app
streamlit run stock_app.py

# App opens at http://localhost:8501
```

### First Time: What You'll See

1. **Company Selector** (top of page)
   - Dropdown with 5+ companies (AAPL, MSFT, GOOGL, AMZN, TSLA)
   - Select "AAPL" to start

2. **Stock Price Table** (below selector)
   - Shows last 5 days of price data
   - Columns: Date, Open, Close, High, Low
   - Data refreshes when you change companies

3. **Chat Interface** (bottom half)
   - Message input box: "Ask about the stock prices..."
   - Chat history display (empty on first load)

### Try These Questions

The agent has access to stock data and tools. Try asking:

- **Simple queries:**
  - "What is the average price?"
  - "What was the highest price?"
  - "Did the price go up or down?"

- **Analytical questions:**
  - "What is the price trend?"
  - "Show me the daily changes"
  - "What was the price difference from Monday to Friday?"

- **Comparative questions:**
  - "Which is more expensive, Apple or Microsoft?"
  - "How do tech stocks compare?"
  - "Which has the most volatility?"

- **Follow-ups:**
  - Ask one question, see the response
  - Then ask a follow-up: "Why did it move so much?"
  - Agent maintains context from previous messages

### Behind the Scenes

When you ask a question:

1. **Your message** is sent to the Copilot SDK agent
2. **Agent analyzes** your question and decides which tools to call
3. **Tools execute**: Agent calls `get_stock_data()` or `analyze_stock_data()`
4. **Agent responds** with an answer based on tool results
5. **You see**: Agent response + which tools were called

Look for tool callouts in the chat to see what data the agent accessed.

---

## For Users: What This App Demonstrates

This is a **teaching application** that shows:

✅ **Copilot SDK Integration**
- AI agent initialized with local models
- No cloud API calls or subscriptions required

✅ **Tool Registration & Calling**
- Agent has access to custom tools (get_stock_data, analyze_stock_data)
- Tools are called automatically when needed
- Results are fed back to agent for reasoning

✅ **Web UI + AI Interaction**
- Streamlit provides interactive UI
- Chat interface handles natural language
- Data and AI are integrated seamlessly

✅ **Minimalist Design**
- Clean, focused interface
- Core concepts visible (no complex abstractions)
- Good starting point for building on top

---

## Project Structure for Developers

```
stock_app.py              # Main entry point
├── src/
│   ├── stock_data.py    # Stock price data service
│   ├── agent.py         # Copilot SDK agent setup
│   ├── tools.py         # Tool definitions & handlers
│   └── ui/
│       └── components.py # Streamlit UI components
└── tests/
    ├── test_stock_data.py
    ├── test_agent.py
    ├── test_tools.py
    └── test_integration.py
```

### Key Files to Understand

1. **stock_app.py** - Read this first
   - Main Streamlit page
   - Sets up UI layout
   - Manages session state
   - Calls other modules

2. **src/agent.py** - Then read this
   - Initializes Copilot SDK agent
   - Registers tools
   - Shows how to call agent.send_message()

3. **src/tools.py** - Tool implementations
   - get_stock_data: Fetch price data
   - analyze_stock_data: Analyze prices
   - Tool parameter validation

4. **src/stock_data.py** - Data generation
   - Mock data generator (no external APIs)
   - Company list
   - Realistic OHLC prices

5. **tests/** - Test examples
   - Shows how to test each component
   - Agent tool-calling tests
   - Integration tests for full flows

---

## Configuration

### Environment Variables

Create `.env` file in project root (optional):

```env
# Default model to use
DEFAULT_MODEL=claude-haiku-4.5

# Model inference parameters
MODEL_TEMPERATURE=0.7
MODEL_MAX_TOKENS=500

# Streamlit configuration
STREAMLIT_LOGGER_LEVEL=info
```

### Changing Models

In the Streamlit app:
1. Look for model selector (usually in sidebar)
2. Choose from available local models
3. Selection persists during session

### Adding Companies

To add more companies:
1. Edit `src/stock_data.py`: `COMPANIES` list
2. Mock data generator automatically covers new companies
3. Dropdown updates on app reload

---

## Troubleshooting

### Issue: "Copilot SDK not found"
```
ModuleNotFoundError: No module named 'copilot_sdk'
```
**Solution**: Verify SDK is installed: `pip install copilot-sdk`

### Issue: Model inference too slow
```
Agent response taking >10 seconds
```
**Solution**: 
- Switch to faster model (Claude Haiku 4.5 is fastest)
- Check system resources (CPU/RAM available)
- See `src/agent.py` for timeout configuration

### Issue: "Company not found"
```
Company symbol 'INVALID' not found
```
**Solution**: Check dropdown list. Only 5 companies supported in demo.

### Issue: Chat window empty
```
Nothing displays in chat area
```
**Solution**: 
- Ask a question and click Submit
- Check browser console for JavaScript errors
- Reload page (Ctrl+Shift+R or Cmd+Shift+R)

### Issue: Stock prices seem too realistic/unrealistic
This is expected—prices are randomly generated within realistic ranges for demo purposes. To use real data:
1. Replace `src/stock_data.py` with yfinance API calls
2. Add request library to requirements.txt
3. Handle API rate limits

---

## Next Steps After Understanding the Code

1. **Add a new tool**: Implement in `tools.py` and register in `agent.py`
2. **Add a new company**: Add to COMPANIES list in `stock_data.py`
3. **Modify UI**: Edit `stock_app.py` or `ui/components.py`
4. **Switch models**: Change `DEFAULT_MODEL` in agent.py
5. **Extend chat context**: Add more context fields to agent.send_message() call

---

## Performance Tips

- **Agent responses**:
  - Shorter context → faster responses
  - Use Claude Haiku 4.5 for quick demo
  - Consider caching tool results if asking similar questions

- **Stock data**:
  - 5 companies, 5 days = 25 data points (fast)
  - Data is pre-generated in memory (no network calls)

- **Streamlit app**:
  - Uses session_state efficiently
  - Reruns only on user interaction
  - No unnecessary API calls

---

## Learning Resources

Inside the code, look for:
- **Type hints**: Every function shows input/output types
- **Docstrings**: Functions explain what they do
- **Comments**: Complex logic has explanatory comments
- **Tests**: Test files show how to test each component

Example from `agent.py`:
```python
def initialize_agent(model: str = "claude-haiku-4.5") -> CopilotAgent:
    """Initialize Copilot SDK agent with tools.
    
    Args:
        model: Local model name (e.g., "claude-haiku-4.5")
        
    Returns:
        CopilotAgent configured with stock data tools
    """
```

---

## Questions?

- **About Copilot SDK?** See [Copilot SDK docs](https://copilot.example.com/docs)
- **About Streamlit?** See [Streamlit docs](https://docs.streamlit.io)
- **Code questions?** Read `src/` files - comments explain design decisions

---

**Ready to start?** Run `streamlit run stock_app.py` and ask the agent a question about Apple stock! 📈

