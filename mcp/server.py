from fastapi import FastAPI
from calculator_tool import calculate

# Model Context Protocol (MCP) Server
# This is a standalone service that hosts tools the AI agents can call.
# Separating tools from the core agent logic makes the system modular and scalable.
app = FastAPI(title="MCP Tool Server")

@app.get("/search")
def search_web(query: str):
    """
    Mock search tool. In a real system, this would call Serper, Brave Search, or Google API.
    For this project, it demonstrates the agent's ability to trigger a tool via a GET request.
    """
    query = query.lower().strip()

    # Pre-defined mock responses for testing.
    mock_data = {
        "capital of france": "Paris is the capital of France.",
        "capital of germany": "Berlin is the capital of Germany.",
        "capital of india": "Delhi is the capital of India."
    }

    return {
        "result": mock_data.get(query, "No data found for this query in our mock search engine.")
    }

@app.post("/calculate")
def calculator_endpoint(data: dict):
    """
    Calculation tool endpoint. Receives a raw math expression and returns the result.
    This demonstrates complex logic processing outside the main LLM workflow.
    """
    expression = data.get("expression")
    
    # Delegate to the logic in calculator_tool.py
    return calculate(expression)