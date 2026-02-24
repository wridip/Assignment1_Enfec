import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api/ask/"

st.set_page_config(page_title="Agentic AI System", layout="wide")

st.title("🤖 Agentic AI Assistant")

if "history" not in st.session_state:
    st.session_state.history = []

question = st.chat_input("Ask something...")

if question:
    with st.spinner("Thinking..."):
        response = requests.post(API_URL, json={"question": question})

    if response.status_code == 200:
        data = response.json()

        st.session_state.history.append({
            "question": data["question"],
            "answer": data["answer"],
            "plan": data["plan"]
        })
    else:
        st.error(response.json())

# Display chat history
for item in st.session_state.history:
    with st.chat_message("user"):
        st.write(item["question"])

    with st.chat_message("assistant"):
        st.write(item["answer"])
        with st.expander("View Plan"):
            st.write(item["plan"])