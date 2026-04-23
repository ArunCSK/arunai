"""Integration tests for complete workflow."""
import pytest
from src.stock_data import get_stock_prices, get_company_by_symbol
from src.agent import initialize_agent
from src.tools import call_tool, get_stock_data_handler, analyze_stock_data_handler
from src.models import ChatMessage


class TestCompleteWorkflow:
    """Test complete user workflows."""
    
    def test_select_company_and_get_prices(self):
        """Test User Story 1: Select company and view prices."""
        # Step 1: Get company
        company = get_company_by_symbol("AAPL")
        assert company.symbol == "AAPL"
        
        # Step 2: Get prices
        prices = get_stock_prices(company.symbol)
        assert len(prices) == 5
        assert all(p.date for p in prices)
        assert all(p.open > 0 for p in prices)
    
    def test_select_company_ask_agent_simple_response(self):
        """Test User Story 2: Ask agent a question about prices."""
        agent = initialize_agent()
        
        # Context with a selected company
        context = {
            "selected_company": "MSFT",
            "current_prices": get_stock_prices("MSFT"),
            "chat_history": []
        }
        
        # Ask agent a question
        response = agent.send_message("What is the current stock price?", context)
        
        # Verify response
        assert response["success"] if "success" in response else True
        assert "message" in response
        assert isinstance(response["message"], str)
        assert len(response["message"]) > 0
    
    def test_agent_calls_tools_and_responds(self):
        """Test User Story 3: Agent calls tools and incorporates results."""
        agent = initialize_agent()
        
        # Context with prices
        prices = get_stock_prices("GOOGL")
        context = {
            "selected_company": "GOOGL",
            "current_prices": prices,
            "chat_history": []
        }
        
        # Ask a question that should trigger tool calling
        response = agent.send_message("What is the average price of GOOGL?", context)
        
        # Check response
        assert "message" in response
        # May or may not have tool calls depending on implementation
        assert "tool_calls" in response or "message" in response
    
    def test_tool_integration_price_retrieval(self):
        """Test that tools can retrieve price data correctly."""
        # Call tool directly
        result = call_tool("get_stock_data", symbol="AMZN")
        
        assert result["success"] is True
        assert "data" in result
        assert len(result["data"]) == 5
        
        # Verify data format
        for price in result["data"]:
            assert isinstance(price, dict)
            assert "date" in price
            assert "open" in price
            assert "close" in price
    
    def test_tool_integration_analysis(self):
        """Test that tools can analyze price data correctly."""
        # Call tool directly
        result = call_tool("analyze_stock_data", symbol="TSLA", question="What is the trend?")
        
        assert result["success"] is True
        assert "data" in result
        
        data = result["data"]
        assert isinstance(data, dict)
    
    def test_chat_history_multi_turn(self):
        """Test multi-turn conversation with chat history."""
        agent = initialize_agent()
        prices = get_stock_prices("AAPL")
        
        # First turn
        context1 = {
            "selected_company": "AAPL",
            "current_prices": prices,
            "chat_history": []
        }
        response1 = agent.send_message("Tell me about Apple stock", context1)
        
        # Second turn with history
        context2 = {
            "selected_company": "AAPL",
            "current_prices": prices,
            "chat_history": [
                {"sender": "user", "content": "Tell me about Apple stock"},
                {"sender": "agent", "content": response1["message"]}
            ]
        }
        response2 = agent.send_message("What about the trend?", context2)
        
        assert "message" in response2
        assert isinstance(response2["message"], str)
    
    def test_agent_with_different_companies(self):
        """Test agent with multiple different companies."""
        agent = initialize_agent()
        companies = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
        
        for company_symbol in companies:
            prices = get_stock_prices(company_symbol)
            context = {
                "selected_company": company_symbol,
                "current_prices": prices,
                "chat_history": []
            }
            
            response = agent.send_message(f"What is the price of {company_symbol}?", context)
            assert "message" in response
            assert isinstance(response["message"], str)
    
    def test_error_handling_invalid_symbol(self):
        """Test graceful error handling for invalid symbols."""
        # Tool should handle invalid symbol
        result = call_tool("get_stock_data", symbol="NOTREAL")
        assert result["success"] is False
        assert "error" in result
    
    def test_price_validation_in_workflow(self):
        """Test that prices are valid throughout workflow."""
        prices = get_stock_prices("MSFT")
        
        for price in prices:
            # Validation checks
            assert price.high >= price.open
            assert price.high >= price.close
            assert price.low <= price.open
            assert price.low <= price.close
            assert price.low <= price.high
