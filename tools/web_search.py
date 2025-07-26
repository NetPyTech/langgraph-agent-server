from tavily import AsyncTavilyClient
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

client = AsyncTavilyClient(os.getenv("TAVILY_API_KEY"))

async def web_search(query: str) -> str:
    """
    Web search tool to get the answer from internet by doing web search.
    
    Args:
        query (str): The question to answer.

    Returns:
        str: The answer to the question.
    """
    try:
        response = await client.search(
            query=query,
            include_answer="advanced",
            include_raw_content="text",
            country="india"
        )
        return response["answer"]
    except Exception as e:
        return f"Error: {str(e)}"