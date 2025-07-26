from langgraph.graph import StateGraph, START, END
from states.main import SystemState

from agents.market_price_agent.graph import market_price_graph
from agents.gov_scheme_agent.graph import gov_scheme_graph

from langgraph.types import interrupt
from langgraph.checkpoint.mongodb import MongoDBSaver

import os
from dotenv import load_dotenv

load_dotenv()


#-------- Get User Input --------
async def get_user_input(state: SystemState):
    """
    Process user input and determine the next agent/step in the workflow.
    
    This function retrieves user input from the state and determines the routing
    based on conversation history. If a previous agent exists, it returns
    to that agent; otherwise, it starts with the intent identifier.
    
    Args:
        state: Current system state containing user input and routing information
        
    Returns:
        Updated state dictionary with routing information
    """
    user_input = interrupt("")
    
    previous = state["routing"]["previous"]
    
    # Determining next agent based on conversation history
    if previous is not None:
        response = {
            "agent_input_output": {
                "user_input": user_input
            },
            "routing": {
                "next": previous,
                "previous": "user_input"
            }
        }
    else:
        response = {
            "routing": {
                "next": END,
                "previous": "user_input"
            }
        }
        
    return response


#------------- Market Price Agent ----------------
async def market_price_agent(state: SystemState):
    """
    Market price agent to get the answer to a question like 'Finding the market price of crops in a specific region on a specific date' and etc....
    
    Args:
        state: Current system state containing user input and routing information
        
    Returns:
        Updated state dictionary with routing information
    """
    return market_price_graph

#---------------- Government Scheme Agent --------------------
async def gov_scheme_agent(state: SystemState):
    """
    ...
    """
    return gov_scheme_graph

#-------------- Router ---------------------
async def agent_router(state: SystemState):
    """
    Router to determine the next agent based on user input.
    
    Args:
        state: Current system state containing user input and routing information
        
    Returns:
        Updated state dictionary with routing information
    """
    agent_name = state.get("agent_name")
    return {"agent_name": agent_name}

#-------------- Graph --------------------
graph = StateGraph(SystemState)

graph.add_node("agent_router",agent_router)
graph.add_node("market_price_agent",market_price_agent)    
graph.add_node("gov_scheme_agent",gov_scheme_agent) 

graph.add_edge(START,"agent_router")

graph.add_conditional_edges(
    "agent_router",
    lambda state: state.get("agent_name"),
    {
        "market_price_agent": "market_price_agent",
        "gov_scheme_agent": "gov_scheme_agent",
        None: END
    }
)

DB_URI = os.environ.get("MONGO_CONNECTION_URL")

#Compile and return the workflow graph
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph.compile(checkpointer=checkpointer)