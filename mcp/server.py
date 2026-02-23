from fastapi import FastAPI
from calculator_tool import calculate

app = FastAPI()

@app.get("/search")
def search_web(query: str):
    mock_data = {
        "capital of France": "Paris is the capital of France.",
        "capital of Germany": "Berlin is the capital of Germany.",
        "capital of India": "Delhi is the capital of India."
    }

    return {
        "result": mock_data.get(query, "No data found.")
    }

@app.post("/calculate")
def calculator_endpoint(data: dict):
    expression = data.get("expression")
    return calculate(expression)