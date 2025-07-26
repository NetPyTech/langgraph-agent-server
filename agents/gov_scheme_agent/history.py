from typing import ClassVar
from storage.redis.agent_history.base import BaseAgentHistory

# History for worker agent
class GovSchemeAgentHistory(BaseAgentHistory):
    agent_type: ClassVar[str] = "gov_scheme_agent"  # Override agent_type for Redis key