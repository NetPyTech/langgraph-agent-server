import json
import logging
from typing import Dict
from ..config import redis_client, MESSAGE_EXPIRY_SECONDS
from .state_key_mapping import get_state_key    

logger = logging.getLogger(__name__)

# Saving routing state to Redis
async def save_routing_state(workflow_id: str, next_agent: str, previous_agent: str) -> bool:
    """
    Saves routing state to Redis with expiration time.
    
    Args:
        workflow_id: The unique identifier for the workflow
        next_agent: The next agent to be called
        previous_agent: The previous agent that was called
        
    Returns:
        bool: True if routing state was saved successfully, False otherwise
    """
    if not workflow_id:
        logger.error("Invalid argument: workflow_id must be provided")
        return False
        
    try:
        key = await get_state_key(workflow_id) + ":routing_state"
        
        # Ensure values are strings
        if isinstance(next_agent, bytes):
            next_agent = next_agent.decode('utf-8')
        if isinstance(previous_agent, bytes):
            previous_agent = previous_agent.decode('utf-8')
        
        # Create routing state dictionary
        routing_state = {
            "next_agent": next_agent,
            "previous_agent": previous_agent
        }
        
        # Serialize to JSON string
        routing_state_json = json.dumps(routing_state)
        
        # Store in Redis with expiration time
        result = redis_client.setex(
            key,
            MESSAGE_EXPIRY_SECONDS,
            routing_state_json
        )
        
        if result:
            logger.debug(f"Successfully saved routing state for workflow: {workflow_id}")
        else:
            logger.warning(f"Redis operation did not confirm success for workflow: {workflow_id}")
            
        return result  # Redis returns True if successful
    except json.JSONDecodeError as e:
        logger.error(f"JSON serialization error for workflow {workflow_id}: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Failed to save routing state to Redis for workflow {workflow_id}: {str(e)}")
        return False

# Loading routing state from Redis
async def load_routing_state(workflow_id: str) -> Dict[str, str]:
    """
    Loads routing state from Redis.
    
    Args:
        workflow_id: The unique identifier for the workflow
        
    Returns:
        Dict[str, str]: Dictionary with next_agent and previous_agent or default empty routing state
    """
    if not workflow_id:
        logger.error("Invalid argument: workflow_id must be provided")
        return {"next_agent": "", "previous_agent": ""}
    
    try:
        key = await get_state_key(workflow_id) + ":routing_state"
        
        # Retrieve from Redis
        routing_state_json = redis_client.get(key)
        
        if not routing_state_json:
            logger.debug(f"No routing state found for workflow: {workflow_id}")
            return {"next_agent": "", "previous_agent": ""}
            
        # Reset expiration time on access
        try:
            redis_client.expire(key, MESSAGE_EXPIRY_SECONDS)
        except Exception as e:
            logger.warning(f"Failed to reset expiration for key {key}: {str(e)}")
            # Continue since the data was retrieved successfully
        
        # Decode bytes to string if needed
        if isinstance(routing_state_json, bytes):
            routing_state_json = routing_state_json.decode('utf-8')
                
        # Parse JSON string to Python object
        routing_state = json.loads(routing_state_json)
        
        # Ensure all values are strings, not bytes
        for k, v in routing_state.items():
            if isinstance(v, bytes):
                routing_state[k] = v.decode('utf-8')
        
        logger.debug(f"Successfully loaded routing state for workflow: {workflow_id}")        
        return routing_state
    
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error for workflow {workflow_id}: {str(e)}")
        return {"next_agent": "", "previous_agent": ""}
    except Exception as e:
        logger.error(f"Failed to load routing state from Redis for workflow {workflow_id}: {str(e)}")
        return {"next_agent": "", "previous_agent": ""}
