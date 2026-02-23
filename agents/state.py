from typing import TypedDict, Optional

class AgentState(TypedDict):
    question: str
    plan: Optional[str]
    answer: Optional[str]