"""Unit tests for stock data module."""
import pytest
from datetime import datetime
from src.stock_data import (
    get_stock_prices,
    get_companies,
    get_company_by_symbol,
    COMPANIES
)
from src.models import StockPrice, Company


class TestGetStockPrices:
    """Test stock price retrieval functionality."""
    
    def test_get_stock_prices_returns_five_days(self):
        """Test that get_stock_prices returns exactly 5 prices."""
        prices = get_stock_prices("AAPL")
        assert len(prices) == 5
        assert all(isinstance(p, StockPrice) for p in prices)
    
    def test_get_stock_prices_sorted_by_date_ascending(self):
        """Test that prices are sorted by date in ascending order."""
        prices = get_stock_prices("MSFT")
        assert len(prices) > 0
        
        dates = [p.date for p in prices]
        assert dates == sorted(dates)
    
    def test_get_stock_prices_invalid_symbol_returns_error(self):
        """Test that invalid symbol raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            get_stock_prices("INVALID")
        assert "not found" in str(exc_info.value).lower()
    
    def test_get_stock_prices_price_validation(self):
        """Test that prices are valid (high >= open/close, low <= open/close)."""
        prices = get_stock_prices("GOOGL")
        
        for price in prices:
            # High should be >= open and close
            assert price.high >= price.open, f"High {price.high} < Open {price.open}"
            assert price.high >= price.close, f"High {price.high} < Close {price.close}"
            
            # Low should be <= open and close
            assert price.low <= price.open, f"Low {price.low} > Open {price.open}"
            assert price.low <= price.close, f"Low {price.low} > Close {price.close}"
            
            # Low should be <= high
            assert price.low <= price.high, f"Low {price.low} > High {price.high}"
    
    def test_get_stock_prices_positive_floats(self):
        """Test that all prices are positive floats."""
        prices = get_stock_prices("AMZN")
        
        for price in prices:
            assert isinstance(price.open, float) and price.open > 0
            assert isinstance(price.close, float) and price.close > 0
            assert isinstance(price.high, float) and price.high > 0
            assert isinstance(price.low, float) and price.low > 0
    
    def test_get_stock_prices_deterministic(self):
        """Test that same symbol returns consistent prices."""
        prices1 = get_stock_prices("TSLA", seed=42)
        prices2 = get_stock_prices("TSLA", seed=42)
        
        assert len(prices1) == len(prices2)
        for p1, p2 in zip(prices1, prices2):
            assert p1.open == p2.open
            assert p1.close == p2.close
            assert p1.high == p2.high
            assert p1.low == p2.low
    
    def test_get_stock_prices_different_seeds_produce_different_prices(self):
        """Test that different seeds produce different prices."""
        prices1 = get_stock_prices("AAPL", seed=42)
        prices2 = get_stock_prices("AAPL", seed=99)
        
        # At least one price should differ
        differences = 0
        for p1, p2 in zip(prices1, prices2):
            if p1.open != p2.open or p1.close != p2.close:
                differences += 1
        
        assert differences > 0, "Different seeds should produce different prices"


class TestGetCompanies:
    """Test company list functionality."""
    
    def test_get_companies_returns_list(self):
        """Test that get_companies returns a list."""
        companies = get_companies()
        assert isinstance(companies, list)
        assert len(companies) > 0
    
    def test_get_companies_all_company_objects(self):
        """Test that all items are Company objects."""
        companies = get_companies()
        assert all(isinstance(c, Company) for c in companies)
    
    def test_get_companies_has_required_symbols(self):
        """Test that required companies are present."""
        companies = get_companies()
        symbols = [c.symbol for c in companies]
        
        required = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
        for symbol in required:
            assert symbol in symbols, f"Required company {symbol} not found"


class TestGetCompanyBySymbol:
    """Test company lookup functionality."""
    
    def test_get_company_by_symbol_valid(self):
        """Test getting a company by valid symbol."""
        company = get_company_by_symbol("AAPL")
        assert isinstance(company, Company)
        assert company.symbol == "AAPL"
        assert len(company.name) > 0
    
    def test_get_company_by_symbol_case_insensitive(self):
        """Test that symbol lookup is case-insensitive."""
        company_upper = get_company_by_symbol("AAPL")
        company_lower = get_company_by_symbol("aapl")
        assert company_upper.symbol == company_lower.symbol
    
    def test_get_company_by_symbol_invalid_raises_error(self):
        """Test that invalid symbol raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            get_company_by_symbol("NOTREAL")
        assert "not found" in str(exc_info.value).lower()
    
    def test_get_company_by_symbol_all_required(self):
        """Test getting all required companies by symbol."""
        required = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
        
        for symbol in required:
            company = get_company_by_symbol(symbol)
            assert company.symbol == symbol
            assert isinstance(company.name, str)
            assert len(company.name) > 0
