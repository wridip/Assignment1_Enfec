from fastapi import FastAPI
from calculator_tool import calculate

app = FastAPI()

@app.get("/search")
def search_web(query: str):

    query = query.lower().strip()

    mock_data = {
        "capital of france": "Paris is the capital of France.",
        "capital of germany": "Berlin is the capital of Germany.",
        "capital of india": "Delhi is the capital of India."
    }

    return {
        "result": mock_data.get(query, "No data found.")
    }

@app.post("/calculate")
def calculator_endpoint(data: dict):
    expression = data.get("expression")
    return calculate(expression)