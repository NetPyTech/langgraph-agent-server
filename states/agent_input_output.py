from typing_extensions import TypedDict
from dataclasses import dataclass
from typing import Optional, Any

@dataclass(kw_only=True)
class AgentInputOutput(TypedDict):
    user_input: Any = None
    agent_output: Optional[Any] = None