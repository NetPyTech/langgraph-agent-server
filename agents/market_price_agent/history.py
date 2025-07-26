from typing import ClassVar
from storage.redis.agent_history.base import BaseAgentHistory

# History for worker agent
class MarketPriceAgentHistory(BaseAgentHistory):
    agent_type: ClassVar[str] = "market_price_agent"  # Override agent_type for Redis key