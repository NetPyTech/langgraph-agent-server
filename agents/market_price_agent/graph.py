from states.main import SystemState
from langgraph.graph import END, START, StateGraph
from .agents import market_price_agent
from utils.agent_execution import execute_agent_safely
from .history import MarketPriceAgentHistory

#----------- Market Price Agent -----------------------
async def MarketPriceAgent(state: SystemState):
    """
    Market price agent to get the answer to a question like 'Finding the market price of crops in a specific region on a specific date' and etc....
    
    Args:
        state: Current system state containing user input and routing information
        
    Returns:
        Updated state dictionary with routing information
    """
    # Load or create agent history from Redis
    market_price_agent_history = await MarketPriceAgentHistory.load_or_create(state["workflow_id"])

    user_input = state['agent_input_output']['user_input']

    if user_input:
        prompt = f"""
        # Conversation History
        {market_price_agent_history.messages}
        
        # User Input
        {user_input}
        """

        result = await execute_agent_safely(
            market_price_agent,
            prompt
        )

        # Saving the history
        market_price_agent_history.messages.append({
            "user_input": prompt,
            "agent_response": result.data.model_dump()
        })
        await market_price_agent_history.save(state["workflow_id"])
        
        return {
            'routing': {
                'next': END,
                'previous': 'market_price_agent'
            },
            'agent_input_output': {
                'agent_output': result.data.model_dump()
            }
        }
    
    return {
        'routing': {
            'next': END,
            'previous': 'market_price_agent'
        },
        'agent_input_output': {
            'agent_output': "No data found!!!"
        }
    }
    

#---------- Graph ------------
graph = StateGraph(SystemState)

graph.add_node("market_price_agent",MarketPriceAgent)

graph.add_edge(START,"market_price_agent")
graph.add_edge("market_price_agent",END)

market_price_graph = graph.compile()

