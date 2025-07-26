import logging
from ..config import get_redis_client, MESSAGE_EXPIRY_SECONDS
from .state_key_mapping import get_state_key    

logger = logging.getLogger(__name__)

# saving workflow id in redis
async def save_workflow_name(workflow_id: str, workflow_name: str) -> bool:
    """
    Saves workflow name to Redis with expiration time.
    
    Args:
        workflow_id: The unique identifier for the workflow
        workflow_name: The name of the workflow
        
    Returns:
        bool: True if workflow name was saved successfully, False otherwise
    """
    if not workflow_id:
        logger.error("Invalid argument: workflow_id must be provided")
        return False
        
    try:
        key = await get_state_key(workflow_id) + ":workflow_name"

        # Ensure workflow_name is a string
        if isinstance(workflow_name, bytes):
            workflow_name = workflow_name.decode('utf-8')

        # Get redis client
        redis = await get_redis_client()

        # Store in Redis with expiration time
        result = await redis.setex(
            key, 
            MESSAGE_EXPIRY_SECONDS, 
            workflow_name
        )
        
        if result:
            logger.debug(f"Successfully saved workflow name for workflow: {workflow_id}")
        else:
            logger.warning(f"Redis operation did not confirm success for workflow: {workflow_id}")
            
        return result  # Redis returns True if successful
    except Exception as e:
        logger.error(f"Failed to save workflow name to Redis for workflow {workflow_id}: {str(e)}")
        return False

# loading workflow id from redis
async def load_workflow_name(workflow_id: str) -> str:
    """
    Loads workflow name from Redis.
    
    Args:
        workflow_id: The unique identifier for the workflow
        
    Returns:
        str: The workflow name or empty string if not found
    """
    if not workflow_id:
        logger.error("Invalid argument: workflow_id must be provided")
        return ""
    
    try:
        key = await get_state_key(workflow_id) + ":workflow_name"
        
        # Get redis client
        redis = await get_redis_client()
        
        # Retrieve from Redis
        workflow_name = await redis.get(key)
        
        if not workflow_name:
            logger.debug(f"No workflow name found for workflow: {workflow_id}")
            return ""
            
        # Reset expiration time on access
        try:
            await redis.expire(key, MESSAGE_EXPIRY_SECONDS)
        except Exception as e:
            logger.warning(f"Failed to reset expiration for key {key}: {str(e)}")
            # Continue since the data was retrieved successfully
        
        # Decode bytes to string if needed
        if isinstance(workflow_name, bytes):
            workflow_name = workflow_name.decode('utf-8')
        
        logger.debug(f"Successfully loaded workflow name for workflow: {workflow_id}")        
        return workflow_name
    
    except Exception as e:
        logger.error(f"Failed to load workflow name from Redis for workflow {workflow_id}: {str(e)}")
        return ""
