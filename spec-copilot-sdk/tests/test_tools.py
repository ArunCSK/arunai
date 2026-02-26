"""Unit tests for tool implementation."""
import pytest
from src.tools import (
    get_stock_data_handler,
    analyze_stock_data_handler,
    call_tool
)
from src.stock_data import get_stock_prices


class TestGetStockDataHandler:
    """Test the get_stock_data tool handler."""
    
    def test_get_stock_data_handler_returns_dict(self):
        """Test that handler returns a dictionary with success and data."""
        result = get_stock_data_handler("AAPL")
        
        assert isinstance(result, dict)
        assert "success" in result
    
    def test_get_stock_data_handler_success_case(self):
        """Test get_stock_data handler with valid symbol."""
        result = get_stock_data_handler("MSFT")
        
        assert result["success"] is True
        assert "data" in result
        assert isinstance(result["data"], list)
        assert len(result["data"]) == 5  # Should return 5 days of data
    
    def test_get_stock_data_handler_invalid_symbol(self):
        """Test get_stock_data handler with invalid symbol."""
        result = get_stock_data_handler("INVALID")
        
        assert result["success"] is False
        assert "error" in result
        assert isinstance(result["error"], str)
    
    def test_get_stock_data_handler_data_format(self):
        """Test that returned data has correct format."""
        result = get_stock_data_handler("GOOGL")
        
        if result["success"]:
            data = result["data"]
            for price_data in data:
                assert isinstance(price_data, dict)
                assert "date" in price_data
                assert "open" in price_data
                assert "close" in price_data
                assert "high" in price_data
                assert "low" in price_data
    
    def test_get_stock_data_handler_all_companies(self):
        """Test get_stock_data handler for all supported companies."""
        companies = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
        
        for company in companies:
            result = get_stock_data_handler(company)
            assert result["success"] is True
            assert len(result["data"]) == 5


class TestAnalyzeStockDataHandler:
    """Test the analyze_stock_data tool handler."""
    
    def test_analyze_stock_data_handler_returns_dict(self):
        """Test that handler returns a dictionary."""
        result = analyze_stock_data_handler("AAPL", "What is the average price?")
        
        assert isinstance(result, dict)
        assert "success" in result
    
    def test_analyze_stock_data_handler_success_case(self):
        """Test analyze_stock_data handler with valid inputs."""
        result = analyze_stock_data_handler("MSFT", "What is the average price?")
        
        assert result["success"] is True
        assert "data" in result
    
    def test_analyze_stock_data_handler_average_question(self):
        """Test analyzing average stock price."""
        result = analyze_stock_data_handler("GOOGL", "What is the average price?")
        
        assert result["success"] is True
        data = result["data"]
        assert isinstance(data, dict)
        # Should include average field
        assert any(key in data for key in ["average", "answer"])
    
    def test_analyze_stock_data_handler_trend_question(self):
        """Test analyzing stock price trend."""
        result = analyze_stock_data_handler("AMZN", "Is it trending up or down?")
        
        assert result["success"] is True
        data = result["data"]
        # Should include trend information
        assert any(key in data for key in ["change", "percent_change", "trend", "answer"])
    
    def test_analyze_stock_data_handler_high_low_question(self):
        """Test analyzing high/low prices."""
        result = analyze_stock_data_handler("TSLA", "What was the high and low?")
        
        assert result["success"] is True
        data = result["data"]
        # Should include high/low information
        assert any(key in data for key in ["highest_price", "lowest_price", "answer"])
    
    def test_analyze_stock_data_handler_volatility_question(self):
        """Test analyzing volatility."""
        result = analyze_stock_data_handler("AAPL", "How volatile is this stock?")
        
        assert result["success"] is True
        data = result["data"]
        # Should include volatility information
        assert any(key in data for key in ["volatility_level", "average_range", "answer"])
    
    def test_analyze_stock_data_handler_invalid_symbol(self):
        """Test analyze_stock_data handler with invalid symbol."""
        result = analyze_stock_data_handler("INVALID", "What is the price?")
        
        assert result["success"] is False
        assert "error" in result
    
    def test_analyze_stock_data_handler_includes_prices_data(self):
        """Test that analysis includes the actual prices."""
        result = analyze_stock_data_handler("MSFT", "Average price?")
        
        assert result["success"] is True
        data = result["data"]
        assert "prices" in data or "data" in data or isinstance(data.get("answer"), str)


class TestCallTool:
    """Test the call_tool dispatcher function."""
    
    def test_call_tool_get_stock_data(self):
        """Test calling get_stock_data tool via dispatcher."""
        result = call_tool("get_stock_data", symbol="AAPL")
        
        assert isinstance(result, dict)
        assert "success" in result
    
    def test_call_tool_analyze_stock_data(self):
        """Test calling analyze_stock_data tool via dispatcher."""
        result = call_tool("analyze_stock_data", symbol="MSFT", question="What is the average?")
        
        assert isinstance(result, dict)
        assert "success" in result
    
    def test_call_tool_invalid_tool_name(self):
        """Test calling non-existent tool."""
        result = call_tool("invalid_tool", symbol="AAPL")
        
        # Should handle gracefully, either with error or empty result
        assert isinstance(result, dict)
    
    def test_call_tool_get_stock_data_with_kwargs(self):
        """Test calling get_stock_data with keyword arguments."""
        result = call_tool("get_stock_data", symbol="GOOGL")
        
        assert result["success"] is True
    
    def test_call_tool_analyze_stock_data_with_kwargs(self):
        """Test calling analyze_stock_data with keyword arguments."""
        result = call_tool("analyze_stock_data", symbol="AMZN", question="trend analysis?")
        
        assert result["success"] is True
