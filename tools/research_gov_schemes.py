import aiohttp,os,time
from dotenv import load_dotenv
from typing import Any

load_dotenv()

BASE_URL = os.environ.get("NEXUS_SERVICE_BASE_URL")

async def add_data(workflow_id: str, data: Any) -> dict | str:
    """Append new data to an existing RAG collection.

    Args:
        workflow_id (str): Collection/workflow identifier.
        data (Any): Data to add (string, markdown, dict, list, etc.).

    Returns:
        dict | str: Success response (202) or error string.
    """
    url = f"{BASE_URL}/add-data"
    body = {"workflow_id": workflow_id, "data": data}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body) as response:
                if response.status in (200, 202):
                    # 202 Accepted is expected
                    content_type = response.headers.get("Content-Type", "")
                    if "application/json" in content_type:
                        return await response.json()
                    return await response.text()
                return {"error": f"HTTP {response.status}"}
    except Exception as e:
        return f"Error in add_data: {str(e)}"

async def research_scheme(
    workflow_id: str,
    problem: str,
) -> dict | str:
    """Run synchronous scheme research.

    Args:
        workflow_id (str): Workflow identifier to store under.
        problem (str): Farmer's problem description (required).
    Returns:
        dict | str: Report string or JSON, or error message.
    """
    url = f"{BASE_URL}/scheme-research"

    body = {
        "workflow_id": workflow_id,
        "problem": problem,
        "include_application_methods": True,
        "include_automation_analysis": True,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body) as response:
                if response.status == 200:
                    content_type = response.headers.get("Content-Type", "")
                    if "application/json" in content_type:
                        return await response.json()
                    return await response.text()
                return {"error": f"HTTP {response.status}"}
    except Exception as e:
        return f"Error in research_scheme: {str(e)}"


async def research_gov_schemes(workflow_id: str, problem: str) -> str:
    """
    Research government schemes for farmer's specific problems.

    Args:
        workflow_id (str): Workflow identifier to store under.
        problem (str): Farmer's problem description (required).
    Returns:
        dict | str: Report string or JSON, or error message.
    """
    try:
        scheme_data = await research_scheme(workflow_id, problem)
    
        await add_data(workflow_id, scheme_data)
        time.sleep(10)
    
        return "Research is completed successfully you can use the rag query tool to get the information"
    except Exception as e:
        return f"Error in research_gov_schemes: {str(e)}"

