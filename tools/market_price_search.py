import os
from dotenv import load_dotenv
import aiohttp
import asyncio
import datetime
import pytz
import json
from typing import Optional, Dict, Any

load_dotenv()

url = os.getenv("PERPLEXITY_BASE_URL")
headers = {
    "Authorization": "Bearer " + os.getenv("PERPLEXITY_API_KEY"),
    "Content-Type": "application/json"
}
ist = pytz.timezone('Asia/Kolkata')

async def market_price_search(
    crop: str,
    state: str,
    district: Optional[str] = None,
    market: Optional[str] = None
) -> str:
    """
    Market price search tool to get current market prices of crops in a specific region.
    Returns structured data that can be used for calculations.
    
    Args:
        crop (str): The crop to search for.
        state (str): The state to search for.
        district (Optional[str], optional): The district to search for. Defaults to None.
        market (Optional[str], optional): The market to search for. Defaults to None.
    
    Returns:
        str: Structured market price information with numerical data for calculations.
    """
    # Build location string
    location_parts = [state]
    if district:
        location_parts.insert(0, district)
    location = ", ".join(location_parts)
    
    # Build query based on available parameters
    if district and market:
        query = f"What is the current market price of {crop} in {district}, {state} at {market} market? Today's date is {datetime.datetime.now(ist).strftime('%d-%m-%Y')}."
    elif district:
        query = f"What is the current market price of {crop} in {district}, {state}? Today's date is {datetime.datetime.now(ist).strftime('%d-%m-%Y')}."
    elif market:
        query = f"What is the current market price of {crop} in {state} at {market} market? Today's date is {datetime.datetime.now(ist).strftime('%d-%m-%Y')}."
    else:
        query = f"What is the current market price of {crop} in {state}? Today's date is {datetime.datetime.now(ist).strftime('%d-%m-%Y')}."

    payload = {
        "model": "sonar-pro",
        "messages": [
            {
                "role": "system",
                "content": """
                    You are a market price assistant providing structured crop pricing information.

                    CRITICAL REQUIREMENTS:
                    1. Always provide prices in a clear, structured format that includes numerical values
                    2. Include minimum and maximum prices when available
                    3. Specify the unit of measurement (per kg, per quintal, per ton, etc.)
                    4. Include the date of the price quote
                    5. Mention the specific market/mandi name if available
                    6. Include multiple markets if data is available for comparison

                    REQUIRED OUTPUT FORMAT:
                    - Start with a brief summary
                    - Then provide detailed price breakdown with clear numerical values
                    - Use this structure:

                    CROP: [Crop Name]
                    LOCATION: [District, State] or [State]
                    DATE: [Date]

                    PRICE DETAILS:
                    - Market/Mandi: [Market Name]
                    - Minimum Price: ₹[amount] per [unit]
                    - Maximum Price: ₹[amount] per [unit]
                    - Average Price: ₹[amount] per [unit]
                    - Unit: [kg/quintal/ton/etc.]

                    If multiple markets available, list each separately.

                    IMPORTANT: Always include actual numerical values. If exact prices aren't available, clearly state "Price data not available" rather than giving vague responses.
                """
            },
            {
                "role": "user",
                "content": query
            }
        ],
        "temperature": 0.3,
        "top_p": 0.9,
        "return_images": False,
        "return_related_questions": False,
        "top_k": 0,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 0.5
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    raw_response = data["choices"][0]['message']['content']
                    
                    # Post-process to ensure we have the current date context
                    current_date = datetime.datetime.now(ist).strftime('%d-%m-%Y')
                    processed_response = f"SEARCH DATE: {current_date}\n\n{raw_response}"
                    
                    return processed_response
                else:
                    return f"Error fetching market price data: HTTP {response.status}"
                    
    except Exception as e:
        return f"Error in market price search: {str(e)}"

# Additional helper function to extract numerical values from price responses
async def extract_price_data(price_response: str) -> Dict[str, Any]:
    """
    Extract numerical price data from the market price response for calculations.
    
    Args:
        price_response (str): Raw response from market_price_search
        
    Returns:
        Dict[str, Any]: Structured price data with numerical values
    """
    try:
        # This is a simple extraction function 
        extracted_data = {
            "crop": None,
            "location": None,
            "date": None,
            "markets": [],
            "price_summary": {
                "min_price": None,
                "max_price": None,
                "avg_price": None,
                "unit": None
            },
            "raw_response": price_response
        }
        
        lines = price_response.split('\n')
        
        current_market = {}
        for line in lines:
            line = line.strip()
            
            if line.startswith('CROP:'):
                extracted_data["crop"] = line.split(':', 1)[1].strip()
            elif line.startswith('LOCATION:'):
                extracted_data["location"] = line.split(':', 1)[1].strip()
            elif line.startswith('DATE:') or line.startswith('SEARCH DATE:'):
                extracted_data["date"] = line.split(':', 1)[1].strip()
            elif 'Minimum Price:' in line:
                # Extract numerical value from "₹1500 per quintal" format
                price_text = line.split(':', 1)[1].strip()
                # Simple regex-like extraction (you might want to use actual regex)
                import re
                price_match = re.search(r'₹?(\d+(?:\.\d+)?)', price_text)
                if price_match:
                    current_market["min_price"] = float(price_match.group(1))
            elif 'Maximum Price:' in line:
                price_text = line.split(':', 1)[1].strip()
                import re
                price_match = re.search(r'₹?(\d+(?:\.\d+)?)', price_text)
                if price_match:
                    current_market["max_price"] = float(price_match.group(1))
            elif 'Average Price:' in line:
                price_text = line.split(':', 1)[1].strip()
                import re
                price_match = re.search(r'₹?(\d+(?:\.\d+)?)', price_text)
                if price_match:
                    current_market["avg_price"] = float(price_match.group(1))
            elif 'Unit:' in line:
                current_market["unit"] = line.split(':', 1)[1].strip()
                
            # If we have collected market data, add it to markets list
            if current_market and len(current_market) >= 3:  # At least min, max, and unit
                extracted_data["markets"].append(current_market.copy())
                current_market = {}
        
        # Calculate overall summary if we have market data
        if extracted_data["markets"]:
            all_mins = [m.get("min_price") for m in extracted_data["markets"] if m.get("min_price")]
            all_maxs = [m.get("max_price") for m in extracted_data["markets"] if m.get("max_price")]
            all_avgs = [m.get("avg_price") for m in extracted_data["markets"] if m.get("avg_price")]
            
            if all_mins:
                extracted_data["price_summary"]["min_price"] = min(all_mins)
            if all_maxs:
                extracted_data["price_summary"]["max_price"] = max(all_maxs)
            if all_avgs:
                extracted_data["price_summary"]["avg_price"] = sum(all_avgs) / len(all_avgs)
            if extracted_data["markets"]:
                extracted_data["price_summary"]["unit"] = extracted_data["markets"][0].get("unit", "per quintal")
        
        return extracted_data
        
    except Exception as e:
        return {
            "error": f"Failed to extract price data: {str(e)}",
            "raw_response": price_response
        }

async def get_market_price(
    crop: str,
    state: str,
    district: Optional[str] = None,
    market: Optional[str] = None
) -> Any:
    """
    Market price search tool to get current market prices of crops in a specific region.
    Returns structured data that can be used for calculations.
    
    Args:
        crop (str): The crop to search for.
        state (str): The state to search for.
        district (Optional[str], optional): The district to search for. Defaults to None.
        market (Optional[str], optional): The market to search for. Defaults to None.
    
    Returns:
        str: Structured market price information with numerical data for calculations.
    """

    # Search for market price
    price_info = await market_price_search(crop, state, district, market)
    
    # Extract structured data for calculations
    structured_data = await extract_price_data(price_info)

    return structured_data
