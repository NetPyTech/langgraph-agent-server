import json
import logging
from ..config import redis_client, MESSAGE_EXPIRY_SECONDS
from .state_key_mapping import get_state_key    
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Saving workflow final output in redis
async def save_final_output(workflow_id: str, final_output: Dict[str, Any]) -> bool:
    """
    Saves workflow final output to Redis with expiration time.
    
    Args:
        workflow_id: The unique identifier for the workflow
        final_output: The final output of the workflow
        
    Returns:
        bool: True if final output was saved successfully, False otherwise
    """
    if not workflow_id:
        logger.error("Invalid argument: workflow_id must be provided")
        return False
        
    try:
        key = await get_state_key(workflow_id) + ":final_output"
        
        # Ensure values are strings
        if isinstance(final_output, bytes):
            final_output = final_output.decode('utf-8')
        
        # Serialize to JSON string
        final_output_json = json.dumps(final_output)
        
        # Store in Redis with expiration time
        result = redis_client.setex(
            key,
            MESSAGE_EXPIRY_SECONDS,
            final_output_json
        )
        
        if result:
            logger.debug(f"Successfully saved final output for workflow: {workflow_id}")
        else:
            logger.warning(f"Redis operation did not confirm success for workflow: {workflow_id}")
            
        return result  # Redis returns True if successful
    except json.JSONDecodeError as e:
        logger.error(f"JSON serialization error for workflow {workflow_id}: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Failed to save final output to Redis for workflow {workflow_id}: {str(e)}")
        return False

# Loading workflow final output from redis
async def load_workflow_final_output(workflow_id: str) -> Dict[str, Any]:
    """
    Loads workflow final output from Redis.
    
    Args:
        workflow_id: The unique identifier for the workflow
        
    Returns:
        Dict[str, Any]: The final output of the workflow or an empty dictionary if not found
    """
    if not workflow_id:
        logger.error("Invalid argument: workflow_id must be provided")
        return {}
    
    try:
        key = await get_state_key(workflow_id) + ":final_output"  
        
        # Retrieve from Redis
        final_output_json = redis_client.get(key)
        
        if not final_output_json:
            logger.debug(f"No final output found for workflow: {workflow_id}")
            return {}
            
        # Reset expiration time on access
        try:
            redis_client.expire(key, MESSAGE_EXPIRY_SECONDS)
        except Exception as e:
            logger.warning(f"Failed to reset expiration for key {key}: {str(e)}")
            # Continue since the data was retrieved successfully
        
        # Decode bytes to string if needed
        if isinstance(final_output_json, bytes):
            final_output_json = final_output_json.decode('utf-8')
        
        # Parse JSON string to Python object
        final_output = json.loads(final_output_json)
        
        logger.debug(f"Successfully loaded final output for workflow: {workflow_id}")        
        return final_output
    
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error for workflow {workflow_id}: {str(e)}")
        return {}
    except Exception as e:
        logger.error(f"Failed to load final output from Redis for workflow {workflow_id}: {str(e)}")
        return {}