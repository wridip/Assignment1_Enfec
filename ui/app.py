import streamlit as st
import requests

# The base URL of our Django backend API.
# This should be updated if the Django server runs on a different port.
API_URL = "http://127.0.0.1:8000/api/ask/"

# 1. UI Configuration: Sets the page title and makes the layout wide.
st.set_page_config(page_title="Agentic AI System", layout="wide")

st.title("🤖 Agentic AI Assistant")

# 2. Session State Management: Keeps a history of the chat during the session.
# Streamlit reruns the script on every input; session_state ensures history is preserved.
if "history" not in st.session_state:
    st.session_state.history = []

# 3. Chat Interface: Input box for user questions at the bottom of the screen.
question = st.chat_input("Ask something...")

if question:
    # 🔹 Step 1: Immediate visual feedback (spinner) while the backend processes.
    with st.spinner("Thinking..."):
        try:
            # 🔹 Step 2: POST request to the Django backend.
            response = requests.post(API_URL, json={"question": question})

            if response.status_code == 200:
                # 🔹 Step 3: Success: Update the persistent chat history.
                data = response.json()

                st.session_state.history.append({
                    "question": data["question"],
                    "answer": data["answer"],
                    "plan": data["plan"]
                })
            else:
                # 🔹 Step 4: API-level error handling.
                st.error(f"Backend API Error: {response.json()}")
        except Exception as e:
            # 🔹 Step 5: Network-level error handling.
            st.error(f"Failed to connect to the backend: {str(e)}")

# 4. Display Logic: Render the conversation history as a sequence of chat messages.
# We iterate through the history list and display each turn.
for item in st.session_state.history:
    # Use Streamlit's native 'chat_message' component for a modern look.
    with st.chat_message("user"):
        st.write(item["question"])

    with st.chat_message("assistant"):
        st.write(item["answer"])
        # 'Expander' component allows the user to peek at the internal reasoning (plan).
        with st.expander("View Plan"):
            st.write(item["plan"])