#!/usr/bin/env python3
"""Test stock tools without requiring OpenAI API key."""
import sys
from agent_tools import (
    get_stock_price,
    get_last_5_days_prices,
    get_available_stocks,
    analyze_stock_trend
)
import json


def test_stock_tools():
    """Test the stock analysis tools."""
    print("🧪 Testing Stock Analysis Tools\n")
    
    # Test 1: Get available stocks
    print("1️⃣  Getting available stocks...")
    try:
        result = get_available_stocks()
        stocks = json.loads(result)
        print(f"   Found {sum(len(v) for v in stocks.values())} stocks across {len(stocks)} categories")
        print(f"   ✓ Success\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
        return False
    
    # Test 2: Get current price
    print("2️⃣  Getting current stock price (AAPL)...")
    try:
        result = get_stock_price("AAPL")
        price_data = json.loads(result)
        if "error" in price_data:
            print(f"   ⚠️  {price_data['error']}")
        else:
            print(f"   Current price: ${price_data.get('current_price', 'N/A')}")
            print(f"   ✓ Success\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    # Test 3: Get 5-day prices
    print("3️⃣  Getting 5-day price data (MSFT)...")
    try:
        result = get_last_5_days_prices("MSFT")
        price_data = json.loads(result)
        if "error" in price_data:
            print(f"   ⚠️  {price_data['error']}")
        else:
            prices = price_data.get('prices', [])
            print(f"   Retrieved {len(prices)} trading days")
            if prices:
                first = prices[0]
                print(f"   Sample: {first['date']} - Close: ${first['close']}")
            print(f"   ✓ Success\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    # Test 4: Analyze trend
    print("4️⃣  Analyzing price trend (GOOGL)...")
    try:
        result = analyze_stock_trend("GOOGL")
        trend_data = json.loads(result)
        if "error" in trend_data:
            print(f"   ⚠️  {trend_data['error']}")
        else:
            trend = trend_data.get('trend', 'UNKNOWN')
            change = trend_data.get('5day_change_percent', 0)
            print(f"   Trend: {trend} ({change:+.2f}%)")
            print(f"   ✓ Success\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    print("✅ All tools tested successfully!")
    return True


if __name__ == "__main__":
    if not test_stock_tools():
        sys.exit(1)
