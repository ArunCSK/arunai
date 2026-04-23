# Getting Started - Stock Analysis Dashboard

## Prerequisites ✅

The environment has been set up with:
- ✅ Python 3.12.10 virtual environment
- ✅ All required Python packages installed
- ✅ Stock data tools tested and working
- ✅ Streamlit configuration ready

## One-Time Setup (5 minutes)

### Step 1: Get OpenAI API Key

The agent needs an LLM to answer questions. The easiest way is to use OpenAI's free tier:

1. Go to: https://platform.openai.com/api-keys
2. Sign up (free) or log in
3. Create a new API key
4. Copy the key (starts with `sk-`)

### Step 2: Configure the API Key

Edit the `.env` file in the project root:

```
OPENAI_API_KEY=sk-your-key-here
```

Replace `sk-your-key-here` with your actual API key.

**Alternative**: Use Azure OpenAI or other LLM providers (see README.md for details)

## Running the App

### Option 1: Quick Run (Recommended)

```bash
cd c:\Users\Arun\projects\arunai\copilot-sdk
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

### Option 2: Run with Python directly

```bash
C:/Users/Arun/projects/arunai/copilot-sdk/.venv/Scripts/python.exe -m streamlit run app.py
```

## How to Use the App

### Left Panel - Stock Viewer
1. **Select Company**: Use the dropdown to pick a stock (AAPL, MSFT, GOOGL, etc.)
2. **View Chart**: See interactive candlestick chart of last 5 trading days
3. **View Data**: See exact Open, High, Low, Close prices
4. **See Metrics**: Current price, 5-day change, high, and low

### Right Panel - AI Assistant
1. **Ask Questions**: Type questions about stocks
2. **Agent Responds**: The AI agent uses tools to get real data and answer
3. **View History**: See conversation history

### Example Queries

```
"What's the current price of Apple?"
"Show me Tesla's 5-day trend"
"Compare Microsoft and Google"
"Which tech stocks are trending up?"
"What's the volume traded for NVDA?"
```

## Troubleshooting

### ❌ "API key not set"
- Check your `.env` file has the correct key
- Restart Streamlit (Ctrl+C, then `streamlit run app.py`)
- Verify the key starts with `sk-`

### ❌ "Agent not responding"
- Check your internet connection
- Verify your API key is valid (test on https://platform.openai.com)
- Check you haven't exceeded API quota

### ❌ "Stock data not loading"
- Verify market is open (weekdays during market hours)
- Try a different stock symbol
- Check if yfinance is working: `python -c "import yfinance; print(yfinance.Ticker('AAPL').info)"`

### ❌ "Streamlit command not found"
- Use full path: `C:/Users/Arun/projects/arunai/copilot-sdk/.venv/Scripts/streamlit run app.py`
- Or run: `python -m streamlit run app.py`

## Project Structure

```
copilot-sdk/
├── app.py                  # Main Streamlit UI
├── agent.py                # Copilot SDK agent wrapper
├── agent_tools.py          # Stock data tools
├── requirements.txt        # Dependencies
├── .env                    # Configuration (API keys)
├── .streamlit/config.toml  # Streamlit settings
├── README.md               # Full documentation
├── quick_start.py          # Environment check
└── test_tools.py           # Tool verification
```

## Next Steps

1. **Customize**: Modify `agent_tools.py` to add more financial tools
2. **Deploy**: Deploy to Streamlit Cloud (free)
3. **Extend**: Add portfolio tracking, alerts, news integration
4. **Learn**: Study agent patterns in `agent.py` to build more agents

## Key Technologies

- **Streamlit**: Web UI framework
- **Copilot SDK (Agent Framework)**: AI agent orchestration
- **yfinance**: Stock data API (free, no key needed)
- **OpenAI**: LLM for agent intelligence
- **Plotly**: Interactive charts

## Performance

- **First load**: 3-5 seconds (agent initialization)
- **Stock data**: <1 second (cached during session)
- **Agent response**: 2-10 seconds (LLM latency)
- **Chart rendering**: Instant (client-side)

## Free Usage Tips

**OpenAI Free Tier:**
- Limited monthly credits ($5)
- `gpt-4o-mini` is cheapest and fast
- Each stock query costs ~1-5 cents

**Optimize costs:**
- Use `gpt-3.5-turbo` for simpler queries
- Keep conversations short where possible
- Batch queries when you can

## Security Notes

🔒 **Important:**
- Never commit `.env` with real keys to Git
- API keys are like passwords - keep them secret
- Use GitHub Secrets for CI/CD pipelines
- Rotate keys if accidentally exposed

## Support & Resources

- **Agent Framework**: https://github.com/microsoft/agent-framework
- **Streamlit Docs**: https://docs.streamlit.io/
- **OpenAI API**: https://platform.openai.com/docs/
- **yfinance**: https://github.com/ranaroussi/yfinance

---

**Ready to start?**
```
streamlit run app.py
```

Happy analyzing! 📈
