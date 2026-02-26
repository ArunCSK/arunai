"""Copilot SDK agent initialization and message handling."""
import os
from typing import Dict, Any, Optional, List
from src.tools import TOOL_DEFINITIONS, call_tool
from src.models import ChatMessage


class CopilotAgent:
    """Wrapper around Copilot SDK agent for this application."""
    
    def __init__(self, model: str = "claude-haiku-4.5"):
        """
        Initialize Copilot SDK agent with tools and model configuration.
        
        Args:
            model: Local model name (e.g., "claude-haiku-4.5", "gpt-4o")
        """
        self.model = model
        self.tools = TOOL_DEFINITIONS
        self.temperature = float(os.getenv("MODEL_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("MODEL_MAX_TOKENS", "2048"))
        self.message_history: List[ChatMessage] = []
        
        # In a real implementation, this would initialize the actual Copilot SDK
        # For now, we simulate agent behavior
    
    def send_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Send a message to the agent and get a response.
        
        Args:
            message: User message text
            context: Optional context dict with:
                - selected_company: Current company info
                - current_prices: Current stock prices
                - chat_history: Previous messages
        
        Returns:
            Response dict with:
                - message: Agent response text
                - tool_calls: List of tool invocations (if any)
                - model: Model used
                - usage: Token usage
        """
        if context is None:
            context = {}
        
        # Prepare system prompt with context
        system_prompt = self._build_system_prompt(context)
        
        # In real implementation, would call Copilot SDK here:
        # response = copilot_sdk.chat(
        #     model=self.model,
        #     messages=[{"role": "system", "content": system_prompt}, ...],
        #     tools=self.tools,
        #     temperature=self.temperature,
        #     max_tokens=self.max_tokens
        # )
        
        # For now, simulate agent behavior
        response = self._simulate_agent_response(message, context)
        
        return response
    
    def _build_system_prompt(self, context: Dict[str, Any]) -> str:
        """Build system prompt with context information."""
        prompt = """You are a helpful stock price analyst assistant. 
You have access to tools to retrieve and analyze stock price data.
You can answer questions about stocks using the available tools.

When a user asks about stock prices, retrieve the data using get_stock_data tool.
When they ask for analysis, use analyze_stock_data tool.
Always be helpful and accurate with financial data."""
        
        if "selected_company" in context:
            company_symbol = context["selected_company"]
            # Handle both string (symbol) and dict (full company object) formats
            if isinstance(company_symbol, dict):
                prompt += f"\n\nCurrent company: {company_symbol.get('name', '')} ({company_symbol.get('symbol', '')})"
            else:
                # It's a string symbol
                try:
                    from src.stock_data import get_company_by_symbol
                    company = get_company_by_symbol(company_symbol)
                    prompt += f"\n\nCurrent company: {company.name} ({company.symbol})"
                except (ValueError, ImportError):
                    prompt += f"\n\nCurrent company: {company_symbol}"
        
        if "current_prices" in context:
            prices = context["current_prices"]
            if prices:
                prompt += f"\nLatest {len(prices)} days of price data is available."
        
        return prompt
    
    def _simulate_agent_response(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate agent behavior for demo/testing.
        
        In production, this would call the actual Copilot SDK.
        For demo purposes, we analyze the question and call appropriate tools.
        """
        tool_calls = []
        response_text = ""
        
        # Analyze message to determine which tools to call
        message_lower = message.lower()
        
        # Get company symbol (handle both string and dict formats)
        company = context.get("selected_company", "AAPL")
        if isinstance(company, dict):
            company_symbol = company.get("symbol", "AAPL")
        else:
            company_symbol = company  # It's already a string (symbol)
        
        # If asking about prices/data, call get_stock_data
        if any(word in message_lower for word in ["price", "data", "show", "what is", "what are", "how much"]):
            tool_result = call_tool("get_stock_data", symbol=company_symbol)
            if tool_result.get("success"):
                tool_calls.append({
                    "name": "get_stock_data",
                    "args": {"symbol": company_symbol},
                    "result": tool_result.get("data", [])
                })
                response_text = f"I retrieved the stock data for {company_symbol}. "
            else:
                return {
                    "message": f"I couldn't retrieve data for {company_symbol}.",
                    "tool_calls": [],
                    "model": self.model,
                    "usage": {"input_tokens": 0, "output_tokens": 0}
                }
        
        # If asking for analysis, call analyze_stock_data
        if any(word in message_lower for word in ["average", "trend", "trend", "high", "low", "volatility", "change", "analyze"]):
            tool_result = call_tool("analyze_stock_data", symbol=company_symbol, question=message)
            if tool_result.get("success"):
                tool_calls.append({
                    "name": "analyze_stock_data",
                    "args": {"symbol": company_symbol, "question": message},
                    "result": tool_result.get("data", {})
                })
                response_text += tool_result.get("answer", "Analysis complete.")
            else:
                response_text = tool_result.get("error", "Could not perform analysis.")
        
        # If no tools called, provide contextual response
        if not tool_calls:
            if "ai" in message_lower or "copilot" in message_lower:
                response_text = f"I'm an AI stock analyst assistant. I can help you analyze stock prices for {company_symbol}. Try asking me questions like 'What is the average price?' or 'Did the price go up?'"
            elif "hello" in message_lower or "hi" in message_lower:
                response_text = f"Hello! I'm ready to help you analyze {company_symbol}'s stock data. What would you like to know?"
            else:
                response_text = f"I can analyze {company_symbol}'s stock data for you. Could you ask about prices, trends, averages, or volatility?"
        
        return {
            "message": response_text,
            "tool_calls": tool_calls,
            "model": self.model,
            "usage": {"input_tokens": len(message.split()), "output_tokens": len(response_text.split())}
        }


def initialize_agent(model: Optional[str] = None) -> CopilotAgent:
    """
    Initialize Copilot SDK agent with configuration.
    
    Args:
        model: Model name override (uses DEFAULT_MODEL env var if not provided)
    
    Returns:
        CopilotAgent instance
    """
    if model is None:
        model = os.getenv("DEFAULT_MODEL", "claude-haiku-4.5")
    
    return CopilotAgent(model=model)
