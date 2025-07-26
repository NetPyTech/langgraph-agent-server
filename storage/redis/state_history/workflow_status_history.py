import logging
from ..config import redis_client, get_redis_client, MESSAGE_EXPIRY_SECONDS
from .state_key_mapping import get_state_key    

logger = logging.getLogger(__name__)

# saving workflow status in redis
async def save_workflow_status(workflow_id: str, status: str) -> bool:
    """
    Saves workflow status to Redis with expiration time.
    
    Args:
        workflow_id: The unique identifier for the workflow
        status: The status of the workflow
        
    Returns:
        bool: True if workflow status was saved successfully, False otherwise
    """
    if not workflow_id:
        logger.error("Invalid argument: workflow_id must be provided")
        return False
        
    try:
        key = await get_state_key(workflow_id) + ":status"

        # Ensure status is a string
        if isinstance(status, bytes):
            status = status.decode('utf-8')

        # Store in Redis with expiration time
        result = await redis_client.setex(
            key,
            MESSAGE_EXPIRY_SECONDS,
            status
        )
        
        if result:
            logger.debug(f"Successfully saved workflow status '{status}' for workflow: {workflow_id}")
        else:
            logger.warning(f"Redis operation did not confirm success for workflow: {workflow_id}")
            
        return result  # Redis returns True if successful
    except Exception as e:
        logger.error(f"Failed to save workflow status to Redis for workflow {workflow_id}: {str(e)}")
        return False

# loading workflow status from redis
async def load_workflow_status(workflow_id: str) -> str:
    """
    Load workflow status from Redis.
    
    Args:
        workflow_id: The unique identifier for the workflow
        
    Returns:
        str: The status of the workflow or 'PROCESSING' if not found
    """
    if not workflow_id:
        logger.error("Invalid argument: workflow_id must be provided")
        return "PROCESSING"
    
    try:
        key = await get_state_key(workflow_id) + ":status"
        
        # Get redis client - similar to other modules
        redis = await get_redis_client()
        if not redis:
            logger.error(f"Failed to get Redis client for workflow {workflow_id}")
            return "PROCESSING"
        
        # Retrieve from Redis
        status = await redis.get(key)
        
        if not status:
            logger.debug(f"No workflow status found for workflow: {workflow_id}, returning default 'PROCESSING'")
            return "PROCESSING"
            
        # Reset expiration time on access
        try:
            await redis.expire(key, MESSAGE_EXPIRY_SECONDS)
        except Exception as e:
            logger.warning(f"Failed to reset expiration for key {key}: {str(e)}")
            # Continue since the data was retrieved successfully
        
        # Decode bytes to string if needed
        if isinstance(status, bytes):
            status = status.decode('utf-8')
        
        logger.debug(f"Successfully loaded workflow status '{status}' for workflow: {workflow_id}")        
        return status
    
    except Exception as e:
        logger.error(f"Failed to load workflow status from Redis for workflow {workflow_id}: {str(e)}")
        return "PROCESSING"
