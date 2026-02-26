"""Pytest configuration and fixtures."""
import sys
from pathlib import Path

# Add src to Python path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_copilot_agent():
    """Mock Copilot SDK agent for testing."""
    agent = MagicMock()
    agent.send_message = MagicMock(return_value={
        "message": "Test response",
        "tool_calls": [],
        "model": "claude-haiku-4.5"
    })
    return agent


@pytest.fixture
def sample_stock_prices():
    """Sample stock price data for tests."""
    return [
        {"date": "2026-02-22", "open": 150.0, "close": 151.5, "high": 152.0, "low": 149.5},
        {"date": "2026-02-23", "open": 151.5, "close": 152.8, "high": 153.5, "low": 151.0},
        {"date": "2026-02-24", "open": 152.8, "close": 153.2, "high": 154.0, "low": 152.5},
        {"date": "2026-02-25", "open": 153.2, "close": 151.8, "high": 154.2, "low": 151.5},
        {"date": "2026-02-26", "open": 151.8, "close": 150.5, "high": 152.0, "low": 150.0}
    ]
