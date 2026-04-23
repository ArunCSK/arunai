"""Data models for Stock Agent Chat Application."""
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime


@dataclass
class StockPrice:
    """Represents a single day's stock price data (OHLC format)."""
    date: str              # ISO format: "2026-02-26"
    open: float            # Opening price
    close: float           # Closing price
    high: float            # Daily high
    low: float             # Daily low
    
    def __post_init__(self):
        """Validate price data."""
        if self.open <= 0 or self.close <= 0 or self.high <= 0 or self.low <= 0:
            raise ValueError("All prices must be positive")
        if self.high < max(self.open, self.close):
            raise ValueError("High price must be >= open and close prices")
        if self.low > min(self.open, self.close):
            raise ValueError("Low price must be <= open and close prices")
    
    def __repr__(self) -> str:
        return f"StockPrice({self.date}: O={self.open:.2f} C={self.close:.2f} H={self.high:.2f} L={self.low:.2f})"


@dataclass
class Company:
    """Represents a publicly traded company."""
    symbol: str            # Ticker symbol (e.g., "AAPL")
    name: str              # Full company name (e.g., "Apple Inc.")
    
    def __post_init__(self):
        """Validate company data."""
        if not self.symbol or not 1 <= len(self.symbol) <= 5:
            raise ValueError("Symbol must be 1-5 characters")
        if not self.name:
            raise ValueError("Company name cannot be empty")
    
    def __repr__(self) -> str:
        return f"Company({self.symbol}: {self.name})"


@dataclass
class ChatMessage:
    """Represents a single message in the chat conversation."""
    sender: str                              # "user" or "agent"
    content: str                             # Message text
    timestamp: str                           # ISO timestamp
    tool_calls: Optional[List[dict]] = None  # Agent tool invocations (if any)
    
    def __post_init__(self):
        """Validate message data."""
        if self.sender not in ("user", "agent"):
            raise ValueError("Sender must be 'user' or 'agent'")
        if not self.content or len(self.content) > 4096:
            raise ValueError("Content must be 1-4096 characters")
        # Tool calls should be None for user messages, list for agent
        if self.sender == "user" and self.tool_calls is not None:
            self.tool_calls = None
        if self.sender == "agent" and self.tool_calls is None:
            self.tool_calls = []
    
    def __repr__(self) -> str:
        return f"ChatMessage({self.sender}: {self.content[:50]}...)"


@dataclass
class ToolResult:
    """Represents the result of a tool execution."""
    name: str              # Tool name (e.g., "get_stock_data")
    success: bool          # True if tool executed successfully
    data: dict | list      # Tool output data
    error: Optional[str] = None  # Error message if success=False
    
    def __repr__(self) -> str:
        status = "✓" if self.success else "✗"
        return f"ToolResult({status} {self.name})"
