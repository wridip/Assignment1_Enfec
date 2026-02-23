from .planner_agent import planner_node
from .research_agent import research_node

if __name__ == "__main__":
    questions = [
        "What is 23 * 7?",
        "What is the capital of France?"
    ]

    for question in questions:
        state = {"question": question}

        state.update(planner_node(state))
        state.update(research_node(state))

        print("Final State:", state)
        print("-" * 50)