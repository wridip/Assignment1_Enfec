from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import sys
import os

# Make root directory visible
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from agents.graph import build_graph

app = build_graph()


@api_view(['POST'])
def ask_question(request):
    question = request.data.get("question")

    if not question:
        return Response(
            {"error": "Question is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Call LangGraph
        result = app.invoke({
            "question": question,
            "plan": None,
            "answer": None
        })

        return Response({
            "question": result.get("question"),
            "plan": result.get("plan"),
            "answer": result.get("answer"),
        })

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )