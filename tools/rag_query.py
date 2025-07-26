import aiohttp,os
from dotenv import load_dotenv
from typing import Any

load_dotenv()

BASE_URL = os.environ.get("NEXUS_SERVICE_BASE_URL")

async def rag_query(workflow_id: str,query: str) -> str:
    """
    Rag query tool to get the answer from internet by doing web search.
    
    Args:
        workflow_id (str): The workflow id.
        query (str): The question to answer.

    Returns:
        str: The answer to the question.
    """
    url = f"{BASE_URL}/query-data"
    payload = {"workflow_id": workflow_id, "query": query}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    return data["response"]
                else:
                    return f"Error in rag query: HTTP {response.status}"
    except Exception as e:
        return f"Error in rag query: {str(e)}"


async def confirm_scheme_apply_automation(query: str) -> str:
    """
    Confirm if the scheme can be applied through browser automation or not.
    
    Args:
        query (str): The question to answer.

    Returns:
        str: The answer to the question.
    """
    return f"No this scheme can't be applied through browser automation."
    