import os
from typing import Dict, Any, List, Optional
from fastapi import HTTPException
import base64
import io
from PIL import Image
import traceback
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
from vertexai.generative_models import GenerativeModel, ChatSession, Part

# Setup
GCP_PROJECT = os.environ["GCP_PROJECT"]
GCP_LOCATION = "us-central1"
EMBEDDING_MODEL = "text-embedding-004"
EMBEDDING_DIMENSION = 256
GENERATIVE_MODEL = "gemini-1.5-flash-002"

# (updated with llm-rag's config) Configuration settings for the content generation
generation_config = {
    "max_output_tokens": 8192, # Maximum number of tokens for output
    "temperature": 0.5, # Control randomness in output
    "top_p": 0.95, # Use nucleus sampling
}