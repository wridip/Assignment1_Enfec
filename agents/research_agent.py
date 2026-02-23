import requests

MCP_CALCULATOR_URL = "http://127.0.0.1:8001/calculate"
MCP_SEARCH_URL = "http://127.0.0.1:8001/search"
def research_node(state):
    plan = state["plan"]

    if plan.startswith("CALCULATE:"):
        expression = plan.replace("CALCULATE:", "").strip()

        try:
            response = requests.post(
                MCP_CALCULATOR_URL,
                json={"expression": expression}
            )

            result = response.json()

            if result["status"] == "success":
                return {"answer": str(result["result"])}
            else:
                return {"answer": "Calculation error."}

        except Exception as e:
            return {"answer": f"MCP call failed: {str(e)}"}

    elif plan.startswith("SEARCH:"):
        query = plan.replace("SEARCH:", "").strip()

        try:
            response = requests.get(
                MCP_SEARCH_URL,
                params={"query": query}
            )

            result = response.json()

            return {"answer": result["result"]}

        except Exception as e:
            return {"answer": f"Search failed: {str(e)}"}