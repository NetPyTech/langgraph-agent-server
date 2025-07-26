import logging

logger = logging.getLogger(__name__)

# Key naming conventions
async def get_state_key(workflow_id: str) -> str:
    """
    Generates a Redis key for storing routing state for a specific workflow.
    
    Args:
        workflow_id: The unique identifier for the workflow
        
    Returns:
        str: Formatted Redis key in the pattern "workflow:{workflow_id}"
    """
    return f"workflow:{workflow_id}"