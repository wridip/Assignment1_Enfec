from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation

import sys
import os

from agents.graph import build_graph

# Instantiate the LangGraph workflow during server startup.
# This compiles the graph once and makes it ready to serve requests.
graph_app = build_graph()


@api_view(['POST'])
def ask_question(request):
    """
    Main API entry point for the AI assistant.
    Steps:
    1. Receive a question via POST.
    2. Invoke the compiled LangGraph workflow.
    3. Persist the results (Question, Plan, Answer) to our database.
    4. Return the response to the user interface (Streamlit).
    """
    question = request.data.get("question")

    # Validate input: Ensure a question was provided.
    if not question:
        return Response(
            {"error": "A question is required for processing."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # 🔹 Step 1: Call LangGraph (Wait for it to traverse nodes: Planner → Research)
        # We pass an initial state containing only the user's question.
        result = graph_app.invoke({
            "question": question,
            "plan": None,
            "answer": None
        })

        # 🔹 Step 2: Persistence (Database storage)
        # Store the conversation trail so it can be reviewed/logged later.
        Conversation.objects.create(
            question=question,          # Original user input (unmodified)
            plan=result.get("plan"),    # Strategy decided by the Planner
            answer=result.get("answer"), # Final result from Research (using tools)
        )

        # 🔹 Step 3: Success Response
        # Return all information back to the frontend for display.
        return Response({
            "question": result.get("question"),
            "plan": result.get("plan"),
            "answer": result.get("answer"),
        })

    except Exception as e:
        # Comprehensive error handling for system-wide failures.
        return Response(
            {"error": f"An unexpected error occurred during processing: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )