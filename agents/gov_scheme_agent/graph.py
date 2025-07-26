from states.main import SystemState
from langgraph.graph import END, START, StateGraph
from .agents import gov_scheme_agent
from utils.agent_execution import execute_agent_safely
from .history import GovSchemeAgentHistory


#----------- Gov Scheme Agent -----------------------
async def GovSchemeAgent(state: SystemState):
    # Load or create agent history from Redis
    gov_scheme_agent_history = await GovSchemeAgentHistory.load_or_create(state["workflow_id"])

    workflow_id = state["workflow_id"]
    user_input = state['agent_input_output']['user_input']

    if user_input:
        prompt = f"""
        # Workflow ID
        {workflow_id}

        # Conversation History
        {gov_scheme_agent_history.messages}
        
        # User Input
        {user_input}
        """

        result = await execute_agent_safely(
            gov_scheme_agent,
            prompt
        )

        # Saving the history
        gov_scheme_agent_history.messages.append({
            "user_input": prompt,
            "agent_response": result.data.model_dump()
        })
        await gov_scheme_agent_history.save(state["workflow_id"])
        
        return {
            'routing': {
                'next': END,
                'previous': 'gov_scheme_agent'
            },
            'agent_input_output': {
                'agent_output': result.data.model_dump()
            }
        }
    
    return {
        'routing': {
            'next': END,
            'previous': 'gov_scheme_agent'
        },
        'agent_input_output': {
            'agent_output': "Sorry something went wrong!!!"
        }
    }


#---------- Graph ------------
graph = StateGraph(SystemState)

graph.add_node("gov_scheme_agent",GovSchemeAgent)

graph.add_edge(START,"gov_scheme_agent")
graph.add_edge("gov_scheme_agent",END)

gov_scheme_graph = graph.compile()

