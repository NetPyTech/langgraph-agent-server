import aiohttp,os
from dotenv import load_dotenv
from typing import Any, Optional

load_dotenv()

BASE_URL = os.environ.get("NEXUS_SERVICE_BASE_URL")

async def web_scraper(url_to_scrape: str) -> dict | str:
    """Scrape a website via helper server.

    Args:
        url_to_scrape (str): Full URL of the page to scrape.

    Returns:
        dict | str: Scraped data or error message.
    """
    url = f"{BASE_URL}/scrape"
    params = {"url": url_to_scrape}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params) as response:
                if response.status == 200:
                    content_type = response.headers.get("Content-Type", "")
                    if "application/json" in content_type:
                        return await response.json()
                    return await response.text()
                return {"error": f"HTTP {response.status}"}
    except Exception as e:
        return f"Error in scrape: {str(e)}"