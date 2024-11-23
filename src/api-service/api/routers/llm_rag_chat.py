import os
from fastapi import APIRouter, Header, Query, Body, HTTPException
from fastapi.responses import FileResponse
from typing import Dict, Any, List, Optional
import uuid
import time
from datetime import datetime
import mimetypes
from pathlib import Path
from api.utils.llm_rag_utils import chat, load, agent

# Define Router
router = APIRouter()

@router.post("/chat", include_in_schema=True)
async def chat_with_llm(message: str = Body(...)):
    try:
        print("Input message:", message)  # Log the input message
        # Call the chat function
        llm_response = chat(message)
        return {"response": llm_response}  # Return the LLM response
    except Exception as e:
        # Log the error details
        print(f"Error in chat_with_llm: {str(e)}")
        # Return an HTTP 500 error with the exception message
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/chat_agent")
async def chat_with_llm_agent(message: str = Body(...)):
    try:
        print("Input message:", message)  # Log the input message
        # Call the chat function
        llm_response = agent(message)
        return {"response": llm_response}  # Return the LLM response
    except Exception as e:
        # Log the error details
        print(f"Error in chat_with_llm: {str(e)}")
        # Return an HTTP 500 error with the exception message
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

