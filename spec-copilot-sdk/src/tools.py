"""Tool definitions and handlers for Copilot SDK agent."""
from typing import Dict, Any, List
from src.models import ToolResult, StockPrice
from src.stock_data import get_stock_prices, get_company_by_symbol


def get_stock_data_handler(symbol: str) -> Dict[str, Any]:
    """
    Handle get_stock_data tool call - fetch stock prices for a company.
    
    Args:
        symbol: Stock ticker symbol (e.g., "AAPL")
    
    Returns:
        Dict with stock price data or error
    """
    try:
        prices = get_stock_prices(symbol)
        return {
            "success": True,
            "data": [
                {
                    "date": p.date,
                    "open": p.open,
                    "close": p.close,
                    "high": p.high,
                    "low": p.low
                }
                for p in prices
            ]
        }
    except ValueError as e:
        return {
            "success": False,
            "error": str(e)
        }


def analyze_stock_data_handler(symbol: str, question: str) -> Dict[str, Any]:
    """
    Handle analyze_stock_data tool call - analyze stock prices.
    
    Args:
        symbol: Stock ticker symbol
        question: Analysis question (e.g., "What is the average price?")
    
    Returns:
        Dict with analysis results or error
    """
    try:
        prices = get_stock_prices(symbol)
        
        # Normalize question to lowercase for matching
        q_lower = question.lower()
        
        # Average price analysis
        if any(word in q_lower for word in ["average", "mean", "typical"]):
            closing_prices = [p.close for p in prices]
            avg_price = sum(closing_prices) / len(closing_prices)
            return {
                "success": True,
                "analysis": "average_price",
                "answer": f"The average closing price over 5 days is ${avg_price:.2f}",
                "data": {
                    "average": round(avg_price, 2),
                    "prices": closing_prices
                }
            }
        
        # Trend analysis
        elif any(word in q_lower for word in ["trend", "up", "down", "increase", "decrease", "go"]):
            first_close = prices[0].close
            last_close = prices[-1].close
            change = last_close - first_close
            pct_change = (change / first_close) * 100
            trend = "up" if change > 0 else "down"
            
            return {
                "success": True,
                "analysis": "trend",
                "answer": f"The price went {trend} from ${first_close:.2f} to ${last_close:.2f} ({pct_change:+.2f}%)",
                "data": {
                    "start_price": first_close,
                    "end_price": last_close,
                    "change": round(change, 2),
                    "percent_change": round(pct_change, 2)
                }
            }
        
        # High/Low analysis
        elif any(word in q_lower for word in ["high", "low", "maximum", "minimum", "peak", "bottom"]):
            prices_with_dates = [(p.date, p.high, p.low) for p in prices]
            max_high = max(prices_with_dates, key=lambda x: x[1])
            min_low = min(prices_with_dates, key=lambda x: x[2])
            
            return {
                "success": True,
                "analysis": "high_low",
                "answer": f"Highest: ${max_high[1]:.2f} on {max_high[0]}, Lowest: ${min_low[2]:.2f} on {min_low[0]}",
                "data": {
                    "highest_price": round(max_high[1], 2),
                    "highest_date": max_high[0],
                    "lowest_price": round(min_low[2], 2),
                    "lowest_date": min_low[0]
                }
            }
        
        # Volatility analysis
        elif any(word in q_lower for word in ["volatility", "volatile", "range", "swing"]):
            ranges = [p.high - p.low for p in prices]
            avg_range = sum(ranges) / len(ranges)
            max_range = max(ranges)
            
            return {
                "success": True,
                "analysis": "volatility",
                "answer": f"Average daily range: ${avg_range:.2f}, Max range: ${max_range:.2f}",
                "data": {
                    "average_range": round(avg_range, 2),
                    "max_range": round(max_range, 2),
                    "volatility_level": "high" if avg_range > 5 else "moderate" if avg_range > 2 else "low"
                }
            }
        
        # Default: return summary statistics
        else:
            closes = [p.close for p in prices]
            avg = sum(closes) / len(closes)
            
            return {
                "success": True,
                "analysis": "summary",
                "answer": f"Over the 5-day period, the average closing price was ${avg:.2f}",
                "data": {
                    "summary": "Stock data analyzed",
                    "average": round(avg, 2),
                    "data_points": len(prices)
                }
            }
    
    except ValueError as e:
        return {
            "success": False,
            "error": str(e)
        }


# Tool definitions matching Copilot SDK schema
TOOL_DEFINITIONS = [
    {
        "name": "get_stock_data",
        "description": "Fetch the last 5 days of stock price data (OHLC) for a company by ticker symbol",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)"
                }
            },
            "required": ["symbol"]
        }
    },
    {
        "name": "analyze_stock_data",
        "description": "Analyze stock price data to answer questions about trends, averages, highs, lows, volatility, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock ticker symbol"
                },
                "question": {
                    "type": "string",
                    "description": "The analysis question to answer (e.g., 'What is the average price?', 'Did price go up?')"
                }
            },
            "required": ["symbol", "question"]
        }
    }
]


def call_tool(tool_name: str, **kwargs) -> Dict[str, Any]:
    """
    Call a tool handler with the provided arguments.
    
    Args:
        tool_name: Name of the tool to call
        **kwargs: Tool arguments
    
    Returns:
        ToolResult-compatible dict with success/error
    """
    if tool_name == "get_stock_data":
        return get_stock_data_handler(kwargs.get("symbol", ""))
    elif tool_name == "analyze_stock_data":
        return analyze_stock_data_handler(kwargs.get("symbol", ""), kwargs.get("question", ""))
    else:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}"
        }
