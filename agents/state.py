from typing import TypedDict, Optional

# The AgentState defines the "memory" of our graph. 
# In LangGraph, every node receives this state, modifies it, and returns the update.
class AgentState(TypedDict):
    # The original question asked by the user
    question: str
    
    # The intermediate strategy decided by the Planner (e.g., "CALCULATE: 2+2")
    # This acts as a bridge between thinking (Planner) and doing (Research).
    plan: Optional[str]
    
    # The final result produced by the Research agent after using tools
    answer: Optional[str]