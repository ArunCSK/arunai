"""Reusable Streamlit UI components."""
from typing import Optional, List
import streamlit as st
from src.models import StockPrice, ChatMessage, Company
from src.stock_data import COMPANIES, get_stock_prices


def display_company_selector() -> Optional[str]:
    """
    Display company dropdown selector.
    
    Returns:
        Selected company symbol or None
    """
    symbols = [c.symbol for c in COMPANIES]
    names = [f"{c.symbol} - {c.name}" for c in COMPANIES]
    
    selected = st.selectbox(
        "Select a company to view stock data:",
        options=symbols,
        format_func=lambda x: next(n for n in names if n.startswith(x))
    )
    
    return selected


def display_price_table(prices: List[StockPrice], company_symbol: str = "") -> None:
    """
    Display stock prices in a formatted table.
    
    Args:
        prices: List of StockPrice objects
        company_symbol: Symbol for display header
    """
    if not prices:
        st.info("No price data available. Select a company to load data.")
        return
    
    # Convert to display format
    data = []
    for p in prices:
        data.append({
            "Date": p.date,
            "Open": f"${p.open:.2f}",
            "Close": f"${p.close:.2f}",
            "High": f"${p.high:.2f}",
            "Low": f"${p.low:.2f}"
        })
    
    # Display header
    if company_symbol:
        st.subheader(f"📈 {company_symbol} - Last 5 Days Price Data")
    else:
        st.subheader("📈 Stock Price Data")
    
    # Display table
    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )
    
    # Show summary statistics
    col1, col2, col3, col4 = st.columns(4)
    closing_prices = [p.close for p in prices]
    
    with col1:
        st.metric("Average", f"${sum(closing_prices)/len(closing_prices):.2f}")
    with col2:
        st.metric("High", f"${max(p.high for p in prices):.2f}")
    with col3:
        st.metric("Low", f"${min(p.low for p in prices):.2f}")
    with col4:
        first_close = prices[0].close
        last_close = prices[-1].close
        change = last_close - first_close
        st.metric("5-Day Change", f"${change:.2f}", f"{(change/first_close)*100:+.1f}%")


def display_chat_message(message: ChatMessage) -> None:
    """
    Display a single chat message with proper formatting.
    
    Args:
        message: ChatMessage object to display
    """
    with st.chat_message(message.sender, avatar="🧑" if message.sender == "user" else "🤖"):
        st.write(message.content)
        
        # Display tool calls if present
        if message.tool_calls and message.sender == "agent":
            with st.expander(f"🔧 Tools Used ({len(message.tool_calls)})"):
                for tool_call in message.tool_calls:
                    st.write(f"**Tool:** `{tool_call['name']}`")
                    if tool_call.get("args"):
                        st.write(f"**Args:** {tool_call['args']}")
        
        # Show timestamp subtly
        if message.timestamp:
            st.caption(message.timestamp)


def get_chat_input() -> Optional[str]:
    """
    Get user input from chat input box.
    
    Returns:
        User message or None if not submitted
    """
    user_input = st.chat_input(
        "Ask me about the stock prices...",
        key="chat_input"
    )
    return user_input


def initialize_chat_session_state() -> None:
    """Initialize chat-related session state variables."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "selected_company" not in st.session_state:
        st.session_state.selected_company = COMPANIES[0].symbol
    
    if "stock_prices" not in st.session_state:
        st.session_state.stock_prices = []
    
    if "agent_session" not in st.session_state:
        st.session_state.agent_session = None


def refresh_stock_prices(symbol: str) -> List[StockPrice]:
    """
    Fetch and cache stock prices for a company.
    
    Args:
        symbol: Company symbol
    
    Returns:
        List of StockPrice objects
    """
    try:
        prices = get_stock_prices(symbol)
        st.session_state.stock_prices = prices
        return prices
    except ValueError as e:
        st.error(f"Error: {str(e)}")
        return []


def add_to_chat_history(message: ChatMessage) -> None:
    """Add a message to chat history in session state."""
    st.session_state.chat_history.append(message)


def get_chat_history() -> List[ChatMessage]:
    """Get current chat history from session state."""
    return st.session_state.chat_history or []


def clear_chat_history() -> None:
    """Clear chat history from session state."""
    st.session_state.chat_history = []
