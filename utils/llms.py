from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider
import os
from dotenv import load_dotenv

load_dotenv()

market_price_llm = GeminiModel(
    'gemini-2.5-flash', 
    provider=GoogleGLAProvider(api_key=os.getenv("GOOGLE_API_KEY"))
)

gov_scheme_llm = GeminiModel(
    'gemini-2.5-flash', 
    provider=GoogleGLAProvider(api_key=os.getenv("GOOGLE_API_KEY"))
)