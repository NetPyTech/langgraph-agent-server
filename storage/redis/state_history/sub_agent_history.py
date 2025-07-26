import logging
from ..config import redis_client, MESSAGE_EXPIRY_SECONDS
from .state_key_mapping import get_state_key    

logger = logging.getLogger(__name__)

# saving sub agent in redis
async def save_sub_agent(workflow_id: str, sub_agent: str) -> bool:
    """
    Saves sub agent to Redis with expiration time.
    
    Args:
        workflow_id: The unique identifier for the workflow
        sub_agent: The sub agent to be saved
        
    Returns:
        bool: True if sub agent was saved successfully, False otherwise
    """
    if not workflow_id:
        logger.error("Invalid argument: workflow_id must be provided")
        return False
        
    try:
        key = await get_state_key(workflow_id) + ":sub_agent"

        # Ensure sub_agent is a string
        if isinstance(sub_agent, bytes):
            sub_agent = sub_agent.decode('utf-8')

        # Store in Redis with expiration time
        result = redis_client.setex(
            key,
            MESSAGE_EXPIRY_SECONDS,
            sub_agent
        )
        
        if result:
            logger.debug(f"Successfully saved sub agent for workflow: {workflow_id}")
        else:
            logger.warning(f"Redis operation did not confirm success for workflow: {workflow_id}")
            
        return result  # Redis returns True if successful
    except Exception as e:
        logger.error(f"Failed to save sub agent to Redis for workflow {workflow_id}: {str(e)}")
        return False

# loading sub agent from redis
async def load_sub_agent(workflow_id: str) -> str:
    """
    Loads sub agent from Redis.
    
    Args:
        workflow_id: The unique identifier for the workflow
        
    Returns:
        str: The sub agent or an empty string if not found
    """
    if not workflow_id:
        logger.error("Invalid argument: workflow_id must be provided")
        return ""
    
    try:
        key = await get_state_key(workflow_id) + ":sub_agent"
        
        # Retrieve from Redis
        sub_agent = redis_client.get(key)
        
        if not sub_agent:
            logger.debug(f"No sub agent found for workflow: {workflow_id}")
            return ""
            
        # Reset expiration time on access
        try:
            redis_client.expire(key, MESSAGE_EXPIRY_SECONDS)
        except Exception as e:
            logger.warning(f"Failed to reset expiration for key {key}: {str(e)}")
            # Continue since the data was retrieved successfully
        
        # Decode bytes to string if needed
        if isinstance(sub_agent, bytes):
            sub_agent = sub_agent.decode('utf-8')
        
        logger.debug(f"Successfully loaded sub agent for workflow: {workflow_id}")        
        return sub_agent
    
    except Exception as e:
        logger.error(f"Failed to load sub agent from Redis for workflow {workflow_id}: {str(e)}")
        return ""