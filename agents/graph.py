from langgraph.graph import StateGraph
from agents.state import AgentState
from agents.planner_agent import planner_node
from agents.research_agent import research_node


def build_graph():
    """
    Constructs and compiles the LangGraph state machine.
    A graph is composed of Nodes (the thinkers/doers) and Edges (the connection logic).
    """

    # 1. Initialize our workflow by binding it to our defined AgentState schema.
    workflow = StateGraph(AgentState)

    # 2. Add our nodes to the workflow. Each node name maps to a Python function.
    # Nodes typically receive the current state and return an update.
    workflow.add_node("planner", planner_node)
    workflow.add_node("research", research_node)

    # 3. Define the path of execution. 
    # Our simple linear flow is: Entry → Planner → Research → End.
    workflow.set_entry_point("planner")
    
    # Static edge: Execution ALWAYS goes from planner to research node.
    workflow.add_edge("planner", "research")

    # 4. Define our finish point. Once research is done, the workflow terminates.
    workflow.set_finish_point("research")

    # 5. Compile everything into a single callable 'app' instance.
    app = workflow.compile()

    return app