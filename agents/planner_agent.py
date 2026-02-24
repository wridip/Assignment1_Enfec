import re
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

# Initialize our LLM (Llama 3 via Ollama)
# Temperature is set to 0 for consistent, reproducible planning output.
llm = ChatOllama(
    model="llama3",
    temperature=0
)

# This prompt guides the LLM to act as a router rather than a general-purpose chatbot.
PLANNER_PROMPT = """
You are a planning assistant.

If the question requires information lookup:
Respond EXACTLY:

SEARCH: <search query>

Do not answer directly.
Return only one line.
"""

def is_math_question(question: str):
    """
    Heuristic check to detect simple arithmetic expressions.
    This bypasses the LLM for faster, more reliable math routing.
    """
    # Detect simple arithmetic patterns like "2+2", "10 / 5", etc.
    math_pattern = r'[\d\.\s\+\-\*\/\%]+'
    return bool(re.search(r'\d+\s*[\+\-\*\/]\s*\d+', question))


def planner_node(state):
    """
    The Planner Node: Decides 'how' to solve the user's question.
    It outputs a 'plan' which determines the tool the next node will use.
    """
    question = state["question"]

    # 🔹 Step 1: Rule-based math detection
    # Why? LLMs can sometimes hallucinate arithmetic; rule-based is 100% accurate for basic math.
    if is_math_question(question):
        # Extract the specific expression (e.g., from "What is 2+2?" extract "2+2")
        expression = re.findall(r'\d+\s*[\+\-\*\/]\s*\d+', question)
        if expression:
            return {"plan": f"CALCULATE: {expression[0]}"}

    # 🔹 Step 2: Otherwise use LLM for general search/knowledge planning
    # If it's not math, we ask the LLM to format it as a SEARCH query.
    messages = [
        SystemMessage(content=PLANNER_PROMPT),
        HumanMessage(content=question)
    ]

    response = llm.invoke(messages)
    output = response.content.strip()

    # Safety fallback: Ensure the output follows the expected tool-calling format.
    if not output.startswith("SEARCH:"):
        output = f"SEARCH: {question}"

    return {"plan": output}