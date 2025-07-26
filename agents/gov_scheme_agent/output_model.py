from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union


class GovSchemeAgentOutput(BaseModel):
    response: str