"""Stock Analysis Web App - Streamlit UI with Copilot SDK Agent."""
import streamlit as st
import pandas as pd
import asyncio
import json
from datetime import datetime, timedelta
import yfinance as yf
import plotly.graph_objects as go

from agent import StockAnalysisAgent


# Configure Streamlit page
st.set_page_config(
    page_title="Stock Analysis Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        gap: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 3px solid #2196f3;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 3px solid #666;
    }
    .message-content {
        flex: 1;
    }
    .message-role {
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
def init_session_state():
    """Initialize Streamlit session state variables."""
    if "agent" not in st.session_state:
        st.session_state.agent = None
    if "agent_initialized" not in st.session_state:
        st.session_state.agent_initialized = False
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "selected_stock" not in st.session_state:
        st.session_state.selected_stock = "AAPL"


async def initialize_agent():
    """Initialize the Copilot agent."""
    if not st.session_state.agent_initialized:
        with st.spinner("Initializing Copilot Agent..."):
            try:
                agent = StockAnalysisAgent()
                await agent.initialize()
                st.session_state.agent = agent
                st.session_state.agent_initialized = True
                st.success("Agent initialized successfully!")
            except Exception as e:
                st.error(f"Failed to initialize agent: {str(e)}")
                st.info("Please ensure OPENAI_API_KEY is set in your environment or .env file")


def get_stock_data(symbol: str) -> pd.DataFrame:
    """Fetch stock data for the last 5 trading days."""
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1wk").tail(5)
        return data
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {str(e)}")
        return None


def plot_stock_chart(data: pd.DataFrame, symbol: str) -> go.Figure:
    """Create an interactive stock price chart."""
    fig = go.Figure()
    
    # Add candlestick trace
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name=symbol,
        increasing_line_color='green',
        decreasing_line_color='red'
    ))
    
    # Update layout
    fig.update_layout(
        title=f"{symbol} - Last 5 Days Price Action",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_white",
        height=400,
        hovermode='x unified',
        xaxis_rangeslider_visible=False
    )
    
    return fig


def create_stock_stats_table(data: pd.DataFrame) -> pd.DataFrame:
    """Create a statistics table for stock data."""
    stats = []
    for date, row in data.iterrows():
        stats.append({
            "Date": date.strftime("%Y-%m-%d"),
            "Open": f"${row['Open']:.2f}",
            "High": f"${row['High']:.2f}",
            "Low": f"${row['Low']:.2f}",
            "Close": f"${row['Close']:.2f}",
            "Volume": f"{int(row['Volume']):,}"
        })
    return pd.DataFrame(stats)


async def send_message_to_agent(user_message: str):
    """Send a message to the agent and get response."""
    if not st.session_state.agent_initialized:
        await initialize_agent()
    
    if st.session_state.agent:
        with st.spinner("Agent is thinking..."):
            try:
                response = await st.session_state.agent.run(user_message)
                return response
            except Exception as e:
                return f"Error getting response from agent: {str(e)}"
    return "Agent not initialized"


def render_stock_section():
    """Render the stock selection and display section."""
    st.header("📈 Stock Price Viewer")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Popular stocks list
        popular_stocks = [
            "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META",
            "JPM", "BAC", "JNJ", "UNH", "NKE", "MCD"
        ]
        selected = st.selectbox(
            "Select a company:",
            popular_stocks,
            index=popular_stocks.index(st.session_state.selected_stock),
            key="stock_selector"
        )
        st.session_state.selected_stock = selected
    
    with col2:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
    
    # Fetch and display stock data
    st.subheader(f"Last 5 Trading Days - {st.session_state.selected_stock}")
    
    data = get_stock_data(st.session_state.selected_stock)
    if data is not None and not data.empty:
        # Display chart
        fig = plot_stock_chart(data, st.session_state.selected_stock)
        st.plotly_chart(fig, use_container_width=True)
        
        # Display stats table
        st.subheader("Price Statistics")
        stats_df = create_stock_stats_table(data)
        st.dataframe(stats_df, use_container_width=True, hide_index=True)
        
        # Calculate and display summary
        col1, col2, col3, col4 = st.columns(4)
        
        first_close = float(data['Close'].iloc[0])
        last_close = float(data['Close'].iloc[-1])
        change = last_close - first_close
        change_percent = (change / first_close) * 100
        
        with col1:
            st.metric("Current Price", f"${last_close:.2f}")
        with col2:
            st.metric("5-Day Change", f"${change:.2f}", f"{change_percent:.2f}%")
        with col3:
            st.metric("5-Day High", f"${float(data['High'].max()):.2f}")
        with col4:
            st.metric("5-Day Low", f"${float(data['Low'].min()):.2f}")


def render_chat_section():
    """Render the chat interface with the Copilot agent."""
    st.header("💬 AI Stock Assistant")
    
    # Chat history display
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <div class="message-content">
                        <div class="message-role">You</div>
                        <div>{message['content']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <div class="message-content">
                        <div class="message-role">Copilot Agent</div>
                        <div>{message['content']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    st.divider()
    user_input = st.text_input(
        "Ask about stocks:",
        placeholder="e.g., What's the current price of Apple? Show me MSFT 5-day trend...",
        key="user_input"
    )
    
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Get agent response
        agent_response = asyncio.run(send_message_to_agent(user_input))
        
        # Add agent response to history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": agent_response
        })
        
        # Rerun to display the messages
        st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()


def main():
    """Main app function."""
    init_session_state()
    
    # Title and description
    st.title("📊 Stock Analysis Dashboard")
    st.markdown("""
    **Powered by Copilot SDK Agent** - Your AI-powered stock analysis assistant
    
    Select a company to view its 5-day price history, or chat with the AI agent to get insights.
    """)
    
    # Initialize agent
    if not st.session_state.agent_initialized:
        asyncio.run(initialize_agent())
    
    st.divider()
    
    # Main layout
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        render_stock_section()
    
    with col2:
        render_chat_section()
    
    # Footer
    st.divider()
    st.caption("Data provided by yfinance • Powered by Copilot SDK Agent Framework")


if __name__ == "__main__":
    main()
