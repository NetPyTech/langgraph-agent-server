from pydantic_ai import Agent
from dotenv import load_dotenv
from utils.llms import gov_scheme_llm
from .output_model import GovSchemeAgentOutput
from tools.date_time import get_date, get_time
from tools.web_search import web_search
from tools.fire_crawl import web_scraper
from tools.rag_query import rag_query,confirm_scheme_apply_automation
from tools.research_gov_schemes import research_gov_schemes
from tools.browser_use import apply_scheme
from prompts.gov_scheme_agent import gov_scheme_agent_prompt
import logfire
import os

load_dotenv()

logfire.configure(token=os.getenv("LOGFIRE_TOKEN"))

gov_scheme_agent = Agent(
    name="Government Scheme Agent",
    model=gov_scheme_llm,
    system_prompt=gov_scheme_agent_prompt,
    result_type=GovSchemeAgentOutput,
    mcp_servers=[],
    tools=[
        # Date and Time
        get_date,
        get_time,

        # Web search
        web_search,

        # Fire crawl
        web_scraper,

        # Rag query
        rag_query,

        # Confirm scheme apply automation
        confirm_scheme_apply_automation,

        # Research government schemes
        research_gov_schemes,

        # Apply scheme
        apply_scheme
    ],
    retries=5,
    instrument=True
)
gov_scheme_agent.instrument_all()