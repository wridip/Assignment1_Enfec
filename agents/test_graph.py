from agents.graph import build_graph

if __name__ == "__main__":

    app = build_graph()

    result = app.invoke({
        "question": "What is the capital of France?",
        "plan": None,
        "answer": None
    })

    print("Final State:", result)