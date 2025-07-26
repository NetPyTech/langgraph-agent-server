from pydantic_ai import Agent
from dotenv import load_dotenv
from utils.llms import market_price_llm
from .output_model import MarketPriceAgentOutput
from tools.date_time import get_date, get_time
from tools.market_price_search import get_market_price
from tools.web_search import web_search
from prompts.market_price_agent import market_price_agent_prompt
from utils.mcp_client import calculator_mcp
import logfire
import os

load_dotenv()

logfire.configure(token=os.getenv("LOGFIRE_TOKEN"))

market_price_agent = Agent(
    name="Market Price Agent",
    model=market_price_llm,
    system_prompt=market_price_agent_prompt,
    result_type=MarketPriceAgentOutput,
    mcp_servers=[calculator_mcp],
    tools=[
        # Date and Time
        get_date,
        get_time,

        # Market Price Search
        get_market_price,

        # Web search
        web_search   
    ],
    retries=5,
    instrument=True
)
market_price_agent.instrument_all()