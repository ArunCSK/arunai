#!/usr/bin/env python3
"""
DEMO MODE - Run without OpenAI API key to see how the app works

This script demonstrates:
1. Stock data tools in action
2. Agent tool selection and execution
3. Chat interface simulation
"""

import json
from agent_tools import (
    get_stock_price,
    get_last_5_days_prices,
    get_available_stocks,
    analyze_stock_trend,
    get_stock_comparison
)


def print_demo_header():
    """Print demo header."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║       STOCK ANALYSIS DASHBOARD - DEMO MODE                  ║
║                                                              ║
║  This demo shows how the Copilot Agent would respond to     ║
║  stock queries using the available tools. No API key needed!║
╚══════════════════════════════════════════════════════════════╝

This is equivalent to what happens in the web app when you:
1. Type a question in the chat
2. Agent receives the query
3. Agent selects appropriate tools
4. Tools fetch real data from yfinance
5. Agent formats and returns response

Let's see it in action! 📈
""")


def demo_tool_selection_process():
    """Demonstrate how the agent would handle different queries."""
    
    print("\n" + "="*60)
    print("DEMO 1: Price Lookup")
    print("="*60)
    print("\n👤 User: What's the current price of Apple?")
    print("\n🤖 Agent thinks: User wants current price.")
    print("    → I'll use the get_stock_price() tool")
    
    result = get_stock_price("AAPL")
    data = json.loads(result)
    
    print(f"\n🔧 Tool output:")
    print(f"   {json.dumps(data, indent=2)}")
    
    print(f"\n💬 Agent response:")
    if "error" not in data:
        print(f"   Apple (AAPL) is currently trading at ${data['current_price']}")
        print(f"   (Updated: {data['timestamp']})")
    else:
        print(f"   Error: {data['error']}")


def demo_historical_analysis():
    """Demonstrate historical data analysis."""
    
    print("\n" + "="*60)
    print("DEMO 2: 5-Day Price Analysis")
    print("="*60)
    print("\n👤 User: Show me Microsoft's last 5 days of trading")
    print("\n🤖 Agent thinks: User wants detailed historical data.")
    print("    → I'll use the get_last_5_days_prices() tool")
    
    result = get_last_5_days_prices("MSFT")
    data = json.loads(result)
    
    if "error" not in data:
        print(f"\n🔧 Tool output: {len(data['prices'])} trading days retrieved")
        
        # Show summary
        prices = data['prices']
        print(f"\n📊 Summary:")
        print(f"   Period: {prices[0]['date']} to {prices[-1]['date']}")
        print(f"   Opening price: ${prices[0]['open']}")
        print(f"   Closing price: ${prices[-1]['close']}")
        print(f"   High: ${max(p['high'] for p in prices)}")
        print(f"   Low: ${min(p['low'] for p in prices)}")
        
        # Show data table
        print(f"\n   Detailed data:")
        print(f"   {'Date':<12} {'Open':<10} {'High':<10} {'Low':<10} {'Close':<10}")
        print(f"   " + "-"*52)
        for day in prices:
            print(f"   {day['date']:<12} ${day['open']:<9.2f} ${day['high']:<9.2f} ${day['low']:<9.2f} ${day['close']:<9.2f}")
        
        print(f"\n💬 Agent response:")
        print(f"   Microsoft has shown {len(prices)} trading days of data.")
        print(f"   The stock opened at ${prices[0]['open']} and closed at ${prices[-1]['close']}")
        print(f"   Range: ${min(p['low'] for p in prices):.2f} - ${max(p['high'] for p in prices):.2f}")


def demo_stock_comparison():
    """Demonstrate stock comparison."""
    
    print("\n" + "="*60)
    print("DEMO 3: Stock Comparison")
    print("="*60)
    print("\n👤 User: Compare Apple and Google")
    print("\n🤖 Agent thinks: User wants to compare two stocks.")
    print("    → I'll use the get_stock_comparison() tool")
    
    result = get_stock_comparison("AAPL", "GOOGL")
    data = json.loads(result)
    
    if "error" not in data:
        print(f"\n🔧 Tool output:")
        print(json.dumps(data, indent=2))
        
        print(f"\n💬 Agent response:")
        print(f"   Comparison of {data['symbol1']} vs {data['symbol2']}:")
        print(f"")
        print(f"   {data['symbol1']}:")
        print(f"   • Current price: ${data['last_close_1']}")
        print(f"   • 5-day change: {data['5day_change_1']:+.2f}%")
        print(f"")
        print(f"   {data['symbol2']}:")
        print(f"   • Current price: ${data['last_close_2']}")
        print(f"   • 5-day change: {data['5day_change_2']:+.2f}%")


def demo_trend_analysis():
    """Demonstrate trend analysis."""
    
    print("\n" + "="*60)
    print("DEMO 4: Trend Analysis")
    print("="*60)
    print("\n👤 User: Is Tesla going up or down?")
    print("\n🤖 Agent thinks: User wants trend direction.")
    print("    → I'll use the analyze_stock_trend() tool")
    
    result = analyze_stock_trend("TSLA")
    data = json.loads(result)
    
    if "error" not in data:
        print(f"\n🔧 Tool output:")
        print(json.dumps(data, indent=2))
        
        print(f"\n💬 Agent response:")
        trend_emoji = "📈" if data['trend'] == "UPTREND" else "📉" if data['trend'] == "DOWNTREND" else "➡️"
        print(f"   {trend_emoji} Tesla is in a {data['trend']}!")
        print(f"")
        print(f"   • 5-day change: {data['5day_change_percent']:+.2f}%")
        print(f"   • Starting price: ${data['starting_price']:.2f}")
        print(f"   • Ending price: ${data['ending_price']:.2f}")
        print(f"   • 5-day high: ${data['high_5day']:.2f}")
        print(f"   • 5-day low: ${data['low_5day']:.2f}")


def demo_available_stocks():
    """Demonstrate available stocks list."""
    
    print("\n" + "="*60)
    print("DEMO 5: Available Stocks")
    print("="*60)
    print("\n👤 User: What stocks can I look at?")
    print("\n🤖 Agent thinks: User wants a list of available stocks.")
    print("    → I'll use the get_available_stocks() tool")
    
    result = get_available_stocks()
    stocks = json.loads(result)
    
    print(f"\n🔧 Tool output: {sum(len(v) for v in stocks.values())} stocks")
    
    print(f"\n💬 Agent response:")
    print(f"   I have access to {sum(len(v) for v in stocks.values())} popular stocks across {len(stocks)} categories:")
    print(f"")
    for category, symbols in stocks.items():
        print(f"   {category}:")
        print(f"   {', '.join(symbols)}")
        print()


def main():
    """Run the demo."""
    print_demo_header()
    
    try:
        demo_tool_selection_process()
        demo_historical_analysis()
        demo_stock_comparison()
        demo_trend_analysis()
        demo_available_stocks()
        
        print("\n" + "="*60)
        print("✅ DEMO COMPLETE!")
        print("="*60)
        print("""
This is exactly how the Copilot Agent works in the web app!

The key differences when running the full app:

1. 🤖 You interact via natural language in the chat
2. 🧠 The Agent analyzes your question
3. 🔧 The Agent automatically selects the right tools
4. 📊 Tools fetch real data from yfinance
5. 💬 Agent formats and explains the results
6. 💭 Context is maintained across multiple messages

Ready to try the full app?

1️⃣  Edit .env and add your OpenAI API key:
   OPENAI_API_KEY=sk-your-key-here
   
   Get one at: https://platform.openai.com/api-keys

2️⃣  Run the app:
   streamlit run app.py

3️⃣  Start chatting with the stock analyst! 📈

See GETTING_STARTED.md for more details.
""")
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("\nNote: Stock data requires internet connection and yfinance")
        print("Make sure you've run: pip install -r requirements.txt")


if __name__ == "__main__":
    main()
