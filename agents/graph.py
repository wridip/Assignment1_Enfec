from langgraph.graph import StateGraph
from agents.state import AgentState
from agents.planner_agent import planner_node
from agents.research_agent import research_node


def build_graph():

    # Create workflow with defined state
    workflow = StateGraph(AgentState)

    # Register nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("research", research_node)

    # Define execution order
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "research")

    # Define where it ends
    workflow.set_finish_point("research")

    # Compile workflow
    app = workflow.compile()

    return app