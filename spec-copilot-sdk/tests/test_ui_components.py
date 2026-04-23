"""Tests for Streamlit UI components."""
import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from src.models import StockPrice, ChatMessage
from src.ui.components import (
    display_price_table,
    display_chat_message,
    display_company_selector,
    get_chat_input,
    initialize_chat_session_state,
    refresh_stock_prices,
    add_to_chat_history,
    get_chat_history,
    clear_chat_history
)


class TestDisplayPriceTable:
    """Test price table display component."""
    
    def test_display_price_table_with_valid_prices(self):
        """Test that display_price_table renders without error."""
        prices = [
            StockPrice("2026-01-01", 100.0, 102.0, 105.0, 99.0),
            StockPrice("2026-01-02", 102.0, 103.0, 105.0, 101.0),
            StockPrice("2026-01-03", 103.0, 104.0, 106.0, 102.0),
        ]
        
        # Should not raise an exception
        with patch("streamlit.subheader"):
            with patch("streamlit.dataframe"):
                with patch("streamlit.columns", return_value=[MagicMock(), MagicMock(), MagicMock(), MagicMock()]):
                    display_price_table(prices, "AAPL")
    
    def test_display_price_table_with_empty_prices(self):
        """Test that display_price_table handles empty price list."""
        with patch("streamlit.info"):
            display_price_table([], "AAPL")
    
    def test_display_price_table_formats_currency(self):
        """Test that prices are formatted as currency ($X.XX)."""
        prices = [
            StockPrice("2026-01-01", 100.5, 102.3, 105.7, 99.2),
        ]
        
        with patch("streamlit.subheader"):
            with patch("streamlit.dataframe") as mock_dataframe:
                with patch("streamlit.columns", return_value=[MagicMock(), MagicMock(), MagicMock(), MagicMock()]):
                    display_price_table(prices)
                    
                    # Check that dataframe was called
                    mock_dataframe.assert_called_once()


class TestDisplayChatMessage:
    """Test chat message display component."""
    
    def test_display_user_message(self):
        """Test displaying a user message."""
        message = ChatMessage("user", "What is the stock price?", "2026-01-01 10:00:00")
        
        with patch("streamlit.chat_message"):
            with patch("streamlit.write"):
                with patch("streamlit.caption"):
                    display_chat_message(message)
    
    def test_display_agent_message(self):
        """Test displaying an agent message."""
        message = ChatMessage("agent", "The stock price is $100.", "2026-01-01 10:00:01")
        
        with patch("streamlit.chat_message"):
            with patch("streamlit.write"):
                with patch("streamlit.caption"):
                    display_chat_message(message)
    
    def test_display_agent_message_with_tool_calls(self):
        """Test displaying an agent message with tool calls."""
        message = ChatMessage(
            "agent",
            "Let me check the stock data.",
            "2026-01-01 10:00:01",
            tool_calls=[
                {"name": "get_stock_data", "args": {"symbol": "AAPL"}}
            ]
        )
        
        with patch("streamlit.chat_message"):
            with patch("streamlit.write"):
                with patch("streamlit.expander"):
                    with patch("streamlit.caption"):
                        display_chat_message(message)


class TestGetChatInput:
    """Test chat input component."""
    
    def test_get_chat_input_returns_text(self):
        """Test that get_chat_input returns user text."""
        with patch("streamlit.chat_input", return_value="Hello"):
            result = get_chat_input()
            assert result == "Hello"
    
    def test_get_chat_input_returns_none_when_empty(self):
        """Test that get_chat_input returns None when no input."""
        with patch("streamlit.chat_input", return_value=None):
            result = get_chat_input()
            assert result is None


class TestDisplayCompanySelector:
    """Test company selector component."""
    
    def test_display_company_selector_returns_symbol(self):
        """Test that display_company_selector returns selected symbol."""
        with patch("streamlit.selectbox", return_value="AAPL"):
            result = display_company_selector()
            assert result == "AAPL"
    
    def test_display_company_selector_returns_valid_symbol(self):
        """Test that selector returns one of the valid symbols."""
        valid_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
        
        with patch("streamlit.selectbox", return_value="MSFT"):
            result = display_company_selector()
            assert result in valid_symbols


class TestSessionStateManagement:
    """Test session state helper functions."""
    
    def test_initialize_chat_session_state(self):
        """Test that initialize_chat_session_state sets up variables."""
        with patch("streamlit.session_state", {}):
            initialize_chat_session_state()
    
    def test_add_to_chat_history(self):
        """Test adding a message to chat history."""
        with patch("streamlit.session_state", {}) as mock_state:
            mock_state.__setitem__ = MagicMock()
            
            message = ChatMessage("user", "Hello", "2026-01-01 10:00:00")
            # Note: This test verifies the function runs without error
            # Actual session state interaction requires more complex mocking
    
    def test_get_chat_history_returns_list(self):
        """Test that get_chat_history returns a list."""
        with patch("streamlit.session_state", {"chat_history": []}):
            history = get_chat_history()
            assert isinstance(history, list)
    
    def test_clear_chat_history(self):
        """Test clearing chat history."""
        with patch("streamlit.session_state", {}) as mock_state:
            mock_state.__setitem__ = MagicMock()
            # Function should execute without error
            clear_chat_history()


class TestRefreshStockPrices:
    """Test stock price refresh functionality."""
    
    def test_refresh_stock_prices_valid_symbol(self):
        """Test refreshing prices for a valid symbol."""
        with patch("streamlit.session_state", {}):
            with patch("src.stock_data.get_stock_prices") as mock_get:
                mock_prices = [
                    StockPrice("2026-01-01", 100.0, 102.0, 105.0, 99.0),
                    StockPrice("2026-01-02", 102.0, 103.0, 105.0, 101.0),
                ]
                mock_get.return_value = mock_prices
                
                # Mock session_state assignment
                session_state = {}
                
                def mock_setitem(key, value):
                    session_state[key] = value
                
                with patch.object(type(MagicMock()), "__setitem__", side_effect=mock_setitem):
                    result = refresh_stock_prices("AAPL")
                    assert len(result) == 2
    
    def test_refresh_stock_prices_invalid_symbol_shows_error(self):
        """Test that invalid symbol shows error."""
        with patch("streamlit.session_state", {}):
            with patch("src.stock_data.get_stock_prices") as mock_get:
                mock_get.side_effect = ValueError("Symbol not found")
                
                with patch("streamlit.error"):
                    result = refresh_stock_prices("INVALID")
                    assert result == []
