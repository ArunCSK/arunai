"""Stock data tools for the Copilot Agent."""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Annotated
import json


def get_stock_price(
    symbol: Annotated[str, "Stock symbol (e.g., AAPL, MSFT, GOOGL)"],
) -> str:
    """Get the current stock price and basic info for a given symbol."""
    try:
        stock = yf.Ticker(symbol.upper())
        data = stock.history(period="1d")
        
        if data.empty:
            return json.dumps({"error": f"Stock symbol {symbol} not found"})
        
        info = stock.info if hasattr(stock, 'info') else {}
        current_price = data['Close'].iloc[-1]
        
        return json.dumps({
            "symbol": symbol.upper(),
            "current_price": round(float(current_price), 2),
            "currency": info.get("currency", "USD"),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return json.dumps({"error": str(e)})


def get_last_5_days_prices(
    symbol: Annotated[str, "Stock symbol (e.g., AAPL, MSFT, GOOGL)"],
) -> str:
    """Get the last 5 days of OHLC (Open, High, Low, Close) data for a stock."""
    try:
        stock = yf.Ticker(symbol.upper())
        # Get last 7 days to ensure we have 5 business days
        data = stock.history(period="1wk")
        
        if data.empty:
            return json.dumps({"error": f"Stock symbol {symbol} not found"})
        
        # Get last 5 rows (trading days)
        last_5 = data.tail(5)
        
        prices = []
        for date, row in last_5.iterrows():
            prices.append({
                "date": date.strftime("%Y-%m-%d"),
                "open": round(float(row['Open']), 2),
                "high": round(float(row['High']), 2),
                "low": round(float(row['Low']), 2),
                "close": round(float(row['Close']), 2),
                "volume": int(row['Volume'])
            })
        
        return json.dumps({
            "symbol": symbol.upper(),
            "period": "Last 5 trading days",
            "prices": prices,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return json.dumps({"error": str(e)})


def get_stock_comparison(
    symbol1: Annotated[str, "First stock symbol (e.g., AAPL)"],
    symbol2: Annotated[str, "Second stock symbol (e.g., MSFT)"],
) -> str:
    """Compare closing prices of two stocks over the last 5 trading days."""
    try:
        # Get data for both stocks
        stock1 = yf.Ticker(symbol1.upper())
        stock2 = yf.Ticker(symbol2.upper())
        
        data1 = stock1.history(period="1wk").tail(5)
        data2 = stock2.history(period="1wk").tail(5)
        
        if data1.empty or data2.empty:
            return json.dumps({"error": f"Could not find data for {symbol1.upper()} or {symbol2.upper()}"})
        
        comparison = {
            "symbol1": symbol1.upper(),
            "symbol2": symbol2.upper(),
            "last_close_1": round(float(data1['Close'].iloc[-1]), 2),
            "last_close_2": round(float(data2['Close'].iloc[-1]), 2),
            "5day_change_1": round(float((data1['Close'].iloc[-1] - data1['Close'].iloc[0]) / data1['Close'].iloc[0] * 100), 2),
            "5day_change_2": round(float((data2['Close'].iloc[-1] - data2['Close'].iloc[0]) / data2['Close'].iloc[0] * 100), 2),
        }
        
        return json.dumps(comparison)
    except Exception as e:
        return json.dumps({"error": str(e)})


def get_available_stocks() -> str:
    """Get a list of popular stocks available for analysis."""
    popular_stocks = {
        "Technology": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META"],
        "Finance": ["JPM", "BAC", "WFC", "GS", "MS"],
        "Healthcare": ["JNJ", "UNH", "PFE", "ABBV", "TMO"],
        "Industry": ["CAT", "MMM", "BA", "GE"],
        "Other": ["NKE", "MCD", "KO", "PG", "WMT"]
    }
    return json.dumps(popular_stocks)


def analyze_stock_trend(
    symbol: Annotated[str, "Stock symbol (e.g., AAPL)"],
) -> str:
    """Analyze the price trend for a stock over the last 5 trading days."""
    try:
        stock = yf.Ticker(symbol.upper())
        data = stock.history(period="1wk").tail(5)
        
        if data.empty:
            return json.dumps({"error": f"Stock symbol {symbol} not found"})
        
        closes = data['Close'].values
        first_price = float(closes[0])
        last_price = float(closes[-1])
        change_percent = round((last_price - first_price) / first_price * 100, 2)
        
        # Determine trend
        if change_percent > 2:
            trend = "UPTREND"
        elif change_percent < -2:
            trend = "DOWNTREND"
        else:
            trend = "STABLE"
        
        # Find high and low
        high = float(data['High'].max())
        low = float(data['Low'].min())
        
        return json.dumps({
            "symbol": symbol.upper(),
            "trend": trend,
            "5day_change_percent": change_percent,
            "high_5day": round(high, 2),
            "low_5day": round(low, 2),
            "starting_price": round(first_price, 2),
            "ending_price": round(last_price, 2)
        })
    except Exception as e:
        return json.dumps({"error": str(e)})
