"""Copilot SDK Agent for stock analysis."""
import os
import asyncio
from typing import Optional
from agent_framework import ChatAgent
from agent_tools import (
    get_stock_price,
    get_last_5_days_prices,
    get_stock_comparison,
    get_available_stocks,
    analyze_stock_trend
)


class StockAnalysisAgent:
    """Stock analysis agent powered by Copilot SDK."""
    
    def __init__(self, chat_client=None):
        """Initialize the stock analysis agent.
        
        Args:
            chat_client: The chat client to use (OpenAI, Azure, etc.)
                        If None, will try to create one from environment
        """
        self.chat_client = chat_client
        self.agent = None
        self.thread = None
        
    async def initialize(self):
        """Initialize the agent with chat client and tools."""
        # If no client provided, create one from environment variables
        if self.chat_client is None:
            self._setup_client()
        
        # Create agent with stock analysis tools
        self.agent = ChatAgent(
            chat_client=self.chat_client,
            instructions="""You are a helpful stock analysis assistant. You have access to tools that can:
1. Get current stock prices
2. Retrieve last 5 days of OHLC data
3. Compare stocks
4. Analyze price trends
5. List popular stocks

Help users analyze stocks by providing current prices, historical data, and trend analysis.
Always provide accurate information and explain what the data means.
If a user asks about a stock symbol, first check if it's available.
Be precise with numbers and always round to 2 decimal places.""",
            tools=[
                get_stock_price,
                get_last_5_days_prices,
                get_stock_comparison,
                get_available_stocks,
                analyze_stock_trend
            ]
        )
        
        # Create a new thread for multi-turn conversation
        self.thread = self.agent.get_new_thread()
    
    def _setup_client(self):
        """Setup chat client from environment variables."""
        import os
        from pathlib import Path
        
        # Load .env file
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(env_path)
        
        try:
            from openai import AsyncOpenAI
            
            api_key = os.getenv("OPENAI_API_KEY", "").strip()
            if not api_key or api_key.startswith("sk-") and len(api_key) < 20:
                raise ValueError(
                    "OPENAI_API_KEY not configured. "
                    "Please set a valid API key in the .env file. "
                    "Get free API key from https://platform.openai.com/api-keys"
                )
            
            openai_client = AsyncOpenAI(api_key=api_key)
            # Wrap with Agent Framework's OpenAI client
            from agent_framework import OpenAIChatClient
            self.chat_client = OpenAIChatClient(
                client=openai_client,
                model="gpt-4o-mini"  # Free tier model
            )
        except ImportError as e:
            raise ImportError(f"Please install required packages: pip install -r requirements.txt. Error: {e}")
        except Exception as e:
            raise Exception(f"Failed to setup chat client: {str(e)}")
    
    async def run(self, user_input: str) -> str:
        """Run the agent with user input.
        
        Args:
            user_input: The user's question or request
            
        Returns:
            The agent's response
        """
        if not self.agent:
            await self.initialize()
        
        response_text = ""
        async for chunk in self.agent.run_stream(user_input, thread=self.thread):
            if chunk.text:
                response_text += chunk.text
        
        return response_text
    
    async def cleanup(self):
        """Cleanup agent resources."""
        if self.agent:
            await self.agent.close()


async def main():
    """Test the agent."""
    agent = StockAnalysisAgent()
    await agent.initialize()
    
    # Test conversation
    response = await agent.run("What are some popular stocks I can analyze?")
    print("Agent:", response)
    
    response = await agent.run("Show me the last 5 days of prices for Apple (AAPL)")
    print("Agent:", response)
    
    await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
