from typing_extensions import TypedDict
from typing import Literal, Optional
from dataclasses import dataclass
from .agent_input_output import AgentInputOutput
from .routing import Routing

@dataclass(kw_only=True)
class SystemState(TypedDict):
    workflow_id: str
    agent_name: Literal["market_price_agent","gov_scheme_agent"] = None

    routing: Routing
    
    agent_input_output: AgentInputOutput




