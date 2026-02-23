import re
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOllama(
    model="llama3",
    temperature=0
)

PLANNER_PROMPT = """
You are a planning assistant.

If the question requires information lookup:
Respond EXACTLY:

SEARCH: <search query>

Do not answer directly.
Return only one line.
"""

def is_math_question(question: str):
    # Detect simple arithmetic patterns
    math_pattern = r'[\d\.\s\+\-\*\/\%]+'
    return bool(re.search(r'\d+\s*[\+\-\*\/]\s*\d+', question))


def planner_node(state):
    question = state["question"]

    # 🔹 Step 1: Rule-based math detection
    if is_math_question(question):
        # Extract expression (simple version)
        expression = re.findall(r'\d+\s*[\+\-\*\/]\s*\d+', question)
        if expression:
            return {"plan": f"CALCULATE: {expression[0]}"}

    # 🔹 Step 2: Otherwise use LLM for search planning
    messages = [
        SystemMessage(content=PLANNER_PROMPT),
        HumanMessage(content=question)
    ]

    response = llm.invoke(messages)
    output = response.content.strip()

    if not output.startswith("SEARCH:"):
        output = f"SEARCH: {question}"

    return {"plan": output}