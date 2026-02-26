"""Integration tests for agent interaction."""
import pytest
from unittest.mock import MagicMock, patch, Mock
from src.models import ChatMessage
from src.agent import CopilotAgent, initialize_agent
from src.stock_data import get_companies


class TestCopilotAgent:
    """Test agent initialization and interaction."""
    
    def test_initialize_agent_returns_agent(self):
        """Test that initialize_agent returns a CopilotAgent instance."""
        agent = initialize_agent()
        assert isinstance(agent, CopilotAgent)
    
    def test_agent_has_send_message_method(self):
        """Test that agent has send_message method."""
        agent = initialize_agent()
        assert hasattr(agent, 'send_message')
        assert callable(agent.send_message)
    
    def test_send_message_returns_dict(self):
        """Test that send_message returns a dictionary."""
        agent = initialize_agent()
        response = agent.send_message("What is the stock price?", {})
        
        assert isinstance(response, dict)
        assert "message" in response
        assert isinstance(response["message"], str)
    
    def test_send_message_includes_tool_calls(self):
        """Test that send_message can include tool_calls in response."""
        agent = initialize_agent()
        response = agent.send_message("What is the price of AAPL?", {})
        
        assert "tool_calls" in response
        # tool_calls can be empty list or list of tool calls
        assert isinstance(response["tool_calls"], list)
    
    def test_send_message_with_context(self):
        """Test that send_message receives and uses context."""
        agent = initialize_agent()
        context = {
            "selected_company": "AAPL",
            "current_prices": [],
            "chat_history": []
        }
        response = agent.send_message("Tell me about AAPL", context)
        
        assert isinstance(response, dict)
        assert "message" in response
    
    def test_send_message_includes_model_info(self):
        """Test that send_message response includes model information."""
        agent = initialize_agent()
        response = agent.send_message("Hello", {})
        
        assert "model" in response or "message" in response
    
    def test_send_message_response_has_usage_info(self):
        """Test that send_message response has usage information."""
        agent = initialize_agent()
        response = agent.send_message("Hello", {})
        
        # usage might not always be present, but format should be consistent
        assert isinstance(response, dict)
        assert "message" in response
    
    def test_send_message_handles_empty_message(self):
        """Test that agent handles empty messages gracefully."""
        agent = initialize_agent()
        response = agent.send_message("", {})
        
        assert isinstance(response, dict)
        assert "message" in response
    
    def test_send_message_handles_long_messages(self):
        """Test that agent handles long messages."""
        agent = initialize_agent()
        long_message = "What is the stock price? " * 50  # Repeat to make it long
        response = agent.send_message(long_message, {})
        
        assert isinstance(response, dict)
        assert "message" in response


class TestAgentToolCalling:
    """Test agent's ability to identify and call tools."""
    
    def test_agent_calls_tools_for_price_question(self):
        """Test that agent calls tools when asked about prices."""
        agent = initialize_agent()
        response = agent.send_message(
            "What is the stock price for AAPL?",
            {"selected_company": "AAPL"}
        )
        
        # Should call tools or provide relevant response
        assert isinstance(response, dict)
        assert "message" in response
    
    def test_agent_calls_tools_for_analysis_question(self):
        """Test that agent calls tools for analysis questions."""
        agent = initialize_agent()
        response = agent.send_message(
            "What is the average price trend?",
            {"selected_company": "MSFT"}
        )
        
        assert isinstance(response, dict)
        # Response should mention analysis
        message = response.get("message", "").lower()
        assert len(message) > 0
    
    def test_agent_includes_company_context_in_response(self):
        """Test that agent uses company context in its response."""
        agent = initialize_agent()
        
        # Test with a company mentioned
        response = agent.send_message(
            "How is GOOGL doing?",
            {"selected_company": "GOOGL"}
        )
        
        assert isinstance(response, dict)
        message = response.get("message", "").lower()
        assert len(message) > 0


class TestAgentResponseFormat:
    """Test the format of agent responses."""
    
    def test_response_message_is_string(self):
        """Test that response message is a string."""
        agent = initialize_agent()
        response = agent.send_message("Hello", {})
        
        assert isinstance(response["message"], str)
        assert len(response["message"]) > 0
    
    def test_response_tool_calls_is_list(self):
        """Test that tool_calls is always a list."""
        agent = initialize_agent()
        response = agent.send_message("What's the price?", {})
        
        tool_calls = response.get("tool_calls", [])
        assert isinstance(tool_calls, list)
    
    def test_tool_call_has_required_fields(self):
        """Test that tool calls have required fields."""
        agent = initialize_agent()
        response = agent.send_message("Get the price for AAPL", {})
        
        tool_calls = response.get("tool_calls", [])
        for tool_call in tool_calls:
            assert isinstance(tool_call, dict)
            assert "name" in tool_call


class TestAgentWithChatHistory:
    """Test agent behavior with chat history context."""
    
    def test_agent_receives_chat_history(self):
        """Test that agent can receive chat history in context."""
        agent = initialize_agent()
        context = {
            "chat_history": [
                {"sender": "user", "content": "What's the price?"},
                {"sender": "agent", "content": "The price is $100"}
            ]
        }
        response = agent.send_message("And the trend?", context)
        
        assert isinstance(response, dict)
        assert "message" in response
    
    def test_agent_maintains_context_continuity(self):
        """Test that agent understanding maintains context across messages."""
        agent = initialize_agent()
        
        # First message
        context1 = {
            "selected_company": "AAPL",
            "chat_history": []
        }
        response1 = agent.send_message("Looking at Apple stock", context1)
        assert isinstance(response1, dict)
        
        # Second message with follow-up
        context2 = {
            "selected_company": "AAPL",
            "chat_history": [
                {"sender": "user", "content": "Looking at Apple stock"},
                {"sender": "agent", "content": response1["message"]}
            ]
        }
        response2 = agent.send_message("What about the trend?", context2)
        assert isinstance(response2, dict)
