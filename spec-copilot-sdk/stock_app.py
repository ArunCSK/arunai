"""Stock Agent Chat - Main Streamlit Application."""
import streamlit as st
from datetime import datetime
from src.stock_data import get_companies, get_company_by_symbol, get_stock_prices
from src.models import ChatMessage
from src.agent import initialize_agent
from src.ui.components import (
    display_company_selector,
    display_price_table,
    display_chat_message,
    get_chat_input,
    initialize_chat_session_state,
    refresh_stock_prices,
    add_to_chat_history,
    get_chat_history,
)


def initialize_page_config():
    """Initialize Streamlit page configuration."""
    st.set_page_config(
        page_title="Stock Agent Chat",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    st.title("📈 Stock Agent Chat")
    st.markdown(
        "**View stock prices and ask an AI agent questions about stock data.**"
    )


def initialize_session_state():
    """Initialize all session state variables on first run."""
    initialize_chat_session_state()
    
    if "agent" not in st.session_state:
        st.session_state.agent = initialize_agent()
    
    if "selected_company" not in st.session_state:
        st.session_state.selected_company = get_companies()[0].symbol
    
    if "stock_prices" not in st.session_state:
        st.session_state.stock_prices = []


def display_stock_data_section():
    """Display the stock data (prices) section."""
    st.subheader("📊 Stock Price Data")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("**Select Company**")
        selected = display_company_selector()
        
        if selected != st.session_state.selected_company:
            st.session_state.selected_company = selected
            prices = refresh_stock_prices(selected)
            st.session_state.stock_prices = prices
    
    with col2:
        prices = st.session_state.stock_prices
        
        if not prices and st.session_state.selected_company:
            # Load prices on first render
            prices = refresh_stock_prices(st.session_state.selected_company)
            st.session_state.stock_prices = prices
        
        if prices:
            display_price_table(prices, st.session_state.selected_company)
        else:
            st.info(
                f"📌 Select a company to view its stock prices. "
                f"Currently showing data for: {st.session_state.selected_company}"
            )


def display_chat_section():
    """Display the chat interface section."""
    st.subheader("💬 Ask the Agent")
    
    st.markdown(
        f"**Company Selected:** {st.session_state.selected_company}  \n"
        f"Ask questions like: 'What is the average price?' or 'Is it trending up?'"
    )
    
    # Display chat history
    st.markdown("**Conversation**")
    chat_history = get_chat_history()
    
    if chat_history:
        for message in chat_history:
            display_chat_message(message)
    else:
        st.info("Start a conversation by asking about the selected stock.")
    
    # Chat input
    user_input = get_chat_input()
    
    if user_input and user_input.strip():
        # Add user message to history
        user_message = ChatMessage(
            sender="user",
            content=user_input,
            timestamp=datetime.now().strftime("%H:%M:%S")
        )
        add_to_chat_history(user_message)
        
        # Show thinking indicator
        with st.spinner("🤔 Agent is thinking..."):
            try:
                # Build context for agent
                context = {
                    "selected_company": st.session_state.selected_company,
                    "current_prices": st.session_state.stock_prices,
                    "chat_history": [
                        {
                            "sender": msg.sender,
                            "content": msg.content,
                            "timestamp": msg.timestamp
                        }
                        for msg in chat_history[:-1]  # Exclude the current user message
                    ]
                }
                
                # Get agent response
                response = st.session_state.agent.send_message(user_input, context)
                
                # Create agent message
                agent_message = ChatMessage(
                    sender="agent",
                    content=response.get("message", "I apologize, I could not understand that."),
                    timestamp=datetime.now().strftime("%H:%M:%S"),
                    tool_calls=response.get("tool_calls", [])
                )
                add_to_chat_history(agent_message)
                
                # Rerun to display new messages
                st.rerun()
                
            except Exception as e:
                st.error(f"⚠️ Error communicating with agent: {str(e)}")
                st.session_state.chat_history.pop()  # Remove failed user message


def display_sidebar():
    """Display sidebar with app information."""
    with st.sidebar:
        st.markdown("### 📚 About")
        st.markdown(
            "This application demonstrates the **Copilot SDK** by combining:\n\n"
            "- **Stock Data Display**: View 5 days of historical price data\n"
            "- **AI Agent**: Ask natural language questions\n"
            "- **Custom Tools**: Agent can retrieve and analyze stock data"
        )
        
        st.markdown("### ⚙️ Settings")
        debug_mode = st.checkbox("Debug Mode", value=False)
        if debug_mode:
            st.markdown("**Session State**")
            st.json({
                "selected_company": st.session_state.selected_company,
                "num_prices": len(st.session_state.stock_prices),
                "num_messages": len(get_chat_history()),
                "agent_initialized": st.session_state.agent is not None
            })
        
        st.markdown("### 🔗 Links")
        st.markdown(
            "[📖 Documentation](https://github.com/arunai/spec-copilot-sdk)  \n"
            "[🐛 Report Issue](https://github.com/arunai/spec-copilot-sdk/issues)"
        )


def main():
    """Main application entry point."""
    initialize_page_config()
    initialize_session_state()
    
    # Create main layout: data on left, chat on right
    col1, col2 = st.columns([1, 1])
    
    with col1:
        display_stock_data_section()
    
    with col2:
        display_chat_section()
    
    display_sidebar()


if __name__ == "__main__":
    main()
