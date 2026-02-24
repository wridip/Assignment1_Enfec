# Agentic AI System

This project is a multi-agent system built with **LangGraph**, **Django**, **FastAPI (MCP)**, and **Streamlit**. It implements a sophisticated workflow where a **Planner** agent strategizes and a **Research** agent executes tasks using tools via the Model Context Protocol (MCP).

## 🏛️ System Architecture

### User Flow & Architectural Path
According to the project architecture, the data flows as follows:
1. **User types question** in the Streamlit UI.
2. **Streamlit UI** sends a POST request to `/api/ask/`.
3. **Django API** receives the request and invokes the **LangGraph Graph**.
4. **Planner Agent** analyzes the question and generates a structured plan.
5. **Research Agent** receives the plan and executes it by calling the **MCP Tool**.
6. **MCP Tool** (FastAPI) performs the calculation or mock search.
7. **Final Answer** is returned to the graph.
8. **Answer & Plan** are saved to **PostgreSQL**.
9. **Result** is shown back in the **Streamlit UI**.

### Multi-Agent Workflow
- **Planner Agent**: 
    - *Role*: The "Thinker".
    - *Function*: Decides what information is needed to answer the user's question.
    - *Constraint*: It does NOT fetch data itself; it only produces structured instructions (e.g., `SEARCH:` or `CALCULATE:`).
- **Research Agent**:
    - *Role*: The "Executor".
    - *Function*: Executes the plan provided by the Planner.
    - *Mechanism*: Performs deterministic execution by calling external tools via HTTP.

### Mental Model
`Research Agent → HTTP call → MCP Tool → Returns JSON`

## 🚀 Features
- **Intelligent Planning**: Uses **Llama 3** (via Ollama) to convert user queries into structured machine instructions.
- **Rule-Based Math Detection**: Bypasses LLM for simple arithmetic to ensure 100% accuracy and reduced hallucination.
- **Model Context Protocol (MCP)**: A structured way for AI agents to use tools, hosted on a separate FastAPI server.
- **Persistence**: All interactions, including the internal "thoughts" (plans) of the agent, are stored in PostgreSQL.
- **Modern UI**: A clean, chat-like interface for real-time interaction.

## 🛠️ Installation

### 1. Set up a Virtual Environment
```bash
python -m venv venv
# Activate (Windows):
venv\Scripts\activate
# Activate (Linux/macOS):
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
pip install langchain-ollama  # Required for the Planner
```

### 3. Set up Ollama
Ensure [Ollama](https://ollama.com/) is running and you have the `llama3` model:
```bash
ollama pull llama3
```

### 4. Database Configuration
The project uses PostgreSQL. Update your credentials in `backend/core/settings.py` if necessary.
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
cd ..
```

## 🏃 How to Run the App

### Step 1: Start the MCP Tool Server
```bash
# Terminal 1
cd mcp
uvicorn server:app --reload --port 8001
```

### Step 2: Start the Django Backend
```bash
# Terminal 2
cd backend
python manage.py runserver 8000
```

### Step 3: Start the Streamlit Frontend
```bash
# Terminal 3
cd ui
streamlit run app.py
```

## 📸 What it looks like
The application features a dark-themed chat interface.
- **User Messages**: Red robot icon with the question.
- **Assistant Messages**: Orange robot icon with the final answer.
- **Inner Reasoning**: An expandable "View Plan" section showing the Planner's structured output (e.g., `SEARCH: Capital of Germany`).

---
*Developed as part of Assignment 1 - AI/ML Internship.*
