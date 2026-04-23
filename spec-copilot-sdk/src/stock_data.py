"""Stock data service providing mock OHLC prices."""
import random
from typing import List
from src.models import StockPrice, Company


# Define supported companies
COMPANIES = [
    Company(symbol="AAPL", name="Apple Inc."),
    Company(symbol="MSFT", name="Microsoft Corporation"),
    Company(symbol="GOOGL", name="Alphabet Inc."),
    Company(symbol="AMZN", name="Amazon.com Inc."),
    Company(symbol="TSLA", name="Tesla Inc."),
]

# Company symbol to index mapping for consistent data generation
COMPANY_SYMBOLS = {c.symbol: c for c in COMPANIES}


def get_stock_prices(symbol: str, seed: int = 42) -> List[StockPrice]:
    """
    Fetch the last 5 days of stock price data for a company.
    
    Args:
        symbol: Stock ticker symbol (e.g., "AAPL")
        seed: Random seed for reproducible data (for testing)
    
    Returns:
        List of 5 StockPrice objects for the last 5 days
    
    Raises:
        ValueError: If symbol not found
    """
    symbol_upper = symbol.upper()
    if symbol_upper not in COMPANY_SYMBOLS:
        valid_symbols = ", ".join([c.symbol for c in COMPANIES])
        raise ValueError(f"Company symbol '{symbol}' not found. Available: {valid_symbols}")
    
    # Use symbol to seed for consistent data per company
    company_seed = seed + hash(symbol_upper) % 1000
    random.seed(company_seed)
    
    # Generate realistic price data
    prices = []
    base_price = 100.0 + (hash(symbol) % 200)  # Base price determined by symbol
    
    dates = ["2026-02-22", "2026-02-23", "2026-02-24", "2026-02-25", "2026-02-26"]
    
    for date in dates:
        # Random daily movement (±5%)
        daily_change = (random.random() - 0.5) * (base_price * 0.05)
        open_price = base_price
        close_price = base_price + daily_change
        
        # High and low with some variance
        high_price = max(open_price, close_price) + random.random() * (base_price * 0.02)
        low_price = min(open_price, close_price) - random.random() * (base_price * 0.02)
        
        # Round to 2 decimals
        price = StockPrice(
            date=date,
            open=round(open_price, 2),
            close=round(close_price, 2),
            high=round(high_price, 2),
            low=round(low_price, 2)
        )
        prices.append(price)
        base_price = close_price  # Next day based on closing price
    
    return prices


def get_companies() -> List[Company]:
    """Get list of all supported companies."""
    return COMPANIES


def get_company_by_symbol(symbol: str) -> Company:
    """
    Get a company by its symbol.
    
    Args:
        symbol: Stock ticker symbol
    
    Returns:
        Company object
    
    Raises:
        ValueError: If symbol not found
    """
    symbol_upper = symbol.upper()
    if symbol_upper not in COMPANY_SYMBOLS:
        raise ValueError(f"Company symbol '{symbol}' not found")
    return COMPANY_SYMBOLS[symbol_upper]


def generate_mock_prices(seed: int = 42) -> dict:
    """
    Generate mock stock prices for all companies.
    
    Args:
        seed: Random seed for reproducibility
    
    Returns:
        Dict mapping symbol -> list of StockPrice objects
    """
    stock_data = {}
    for company in COMPANIES:
        try:
            stock_data[company.symbol] = get_stock_prices(company.symbol, seed)
        except ValueError:
            continue
    return stock_data
