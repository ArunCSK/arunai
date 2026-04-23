"""Copilot SDK agent initialization and message handling."""
import os
from typing import Dict, Any, Optional, List
from src.tools import TOOL_DEFINITIONS, call_tool, get_tool_handlers
from src.models import ChatMessage

try:
    from github_copilot_sdk import CopilotClient
    COPILOT_SDK_AVAILABLE = True
except ImportError:
    COPILOT_SDK_AVAILABLE = False


class CopilotAgent:
    """Wrapper around Copilot SDK agent for this application."""
    
    def __init__(self, model: str = "claude-haiku-4.5", use_sdk: bool = True):
        """
        Initialize Copilot SDK agent with tools and model configuration.
        
        Args:
            model: Model name (e.g., "gpt-4.1", "gpt-4o")
            use_sdk: Whether to use real Copilot SDK (if available)
        """
        self.model = model
        self.tools = TOOL_DEFINITIONS
        self.temperature = float(os.getenv("MODEL_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("MODEL_MAX_TOKENS", "2048"))
        self.message_history: List[ChatMessage] = []
        self.copilot_client = None
        self.session = None
        self.use_sdk = use_sdk and COPILOT_SDK_AVAILABLE
        
        # Initialize Copilot SDK if available and requested
        if self.use_sdk:
            try:
                self._initialize_sdk()
            except Exception as e:
                print(f"Warning: Failed to initialize Copilot SDK: {e}")
                print("Using simulation mode instead")
                self.use_sdk = False
    
    def _initialize_sdk(self):
        """Initialize the Copilot SDK client."""
        from github_copilot_sdk import CopilotClient
        
        # Create SDK client
        cli_url = os.getenv("COPILOT_CLI_URL", "").strip()
        
        if cli_url:
            # Connect to existing CLI server
            self.copilot_client = CopilotClient(cliUrl=cli_url)
        else:
            # Let SDK manage CLI automatically
            self.copilot_client = CopilotClient()
    
    def send_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Send a message to the agent and get a response.
        
        Uses real Copilot SDK if available and configured, otherwise falls back to simulation.
        
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
                - success: Whether the call succeeded
        """
        if context is None:
            context = {}
        
        # Try to use real SDK if available and configured
        if self.use_sdk and self.copilot_client:
            try:
                return self._send_message_with_sdk(message, context)
            except Exception as e:
                print(f"SDK call failed: {e}. Falling back to simulation.")
                self.use_sdk = False
                return self._simulate_agent_response(message, context)
        
        # Fall back to simulation (or if SDK not available)
        return self._simulate_agent_response(message, context)
    
    def _send_message_with_sdk(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send message using real Copilot SDK.
        
        Makes synchronous HTTP call to Copilot CLI or uses synchronous SDK wrapper.
        """
        try:
            # Build system prompt with context
            system_prompt = self._build_system_prompt(context)
            
            # Format full context message
            full_message = f"{system_prompt}\n\nUser question: {message}"
            
            # Send via SDK with tool definitions
            # The SDK will handle tool invocation automatically
            response = self.copilot_client.sendMessage(
                prompt=full_message,
                model=self.model,
                temperature=self.temperature,
                maxTokens=self.max_tokens,
                tools=self.tools
            )
            
            # Parse SDK response
            tool_calls = response.get("toolCalls", []) or []
            response_text = response.get("content", response.get("message", ""))
            
            if not response_text:
                # Fallback if no content
                response_text = f"I processed your request about {context.get('selected_company', 'stock prices')}."
            
            return {
                "success": True,
                "message": response_text,
                "tool_calls": tool_calls,
                "model": self.model,
                "usage": {
                    "input_tokens": len(message.split()),
                    "output_tokens": len(response_text.split())
                }
            }
        except Exception as e:
            # If SDK call fails, fall back gracefully
            return {
                "success": False,
                "message": f"Agent communication error: {str(e)}. Using fallback response.",
                "tool_calls": [],
                "model": self.model,
                "usage": {"input_tokens": 0, "output_tokens": 0}
            }
    
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
