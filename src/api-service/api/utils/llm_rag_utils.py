import os
from typing import Dict, Any, List, Optional
from fastapi import HTTPException
import base64
import io
from PIL import Image
from pathlib import Path
import traceback
import chromadb
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
from vertexai.generative_models import GenerativeModel, ChatSession, Part

# Setup
GCP_PROJECT = os.environ["GCP_PROJECT"]
GCP_LOCATION = "us-central1"
EMBEDDING_MODEL = "text-embedding-004"
EMBEDDING_DIMENSION = 256
GENERATIVE_MODEL = "gemini-1.5-flash-002"
CHROMADB_HOST = os.environ["CHROMADB_HOST"]
CHROMADB_PORT = os.environ["CHROMADB_PORT"]

# (updated with llm-rag's config) Configuration settings for the content generation
generation_config = {
    "max_output_tokens": 8192, # Maximum number of tokens for output
    "temperature": 0.5, # Control randomness in output
    "top_p": 0.95, # Use nucleus sampling
}

# Initialize the GenerativeModel with specific system instructions
SYSTEM_INSTRUCTION = """
You are a knowledgeable music expert who can generate personalized playlists.
Consider the user's mood, interests, and personal music preferences to craft
the perfect playlist. You may use information about song lyrics and artist/song
info in the provided chunks to inform your playlist song selections.

When answering a query:
1. Carefully read all the text chunks provided.
2. Identify the most relevant information from these chunks that aligns with
   the user's music requests. If the genre/artist in the chunks does not match
   the user's request, ignore the chunk.
3. When crafting your response, provide your best song recommendations. You are
   not limited to the songs & information mentioned in the chunks, but you may
   refer to the relevant chunks to justify the song selections. Cite the song
   lyrics or artist annotations if applicable.
4. Provide a playlist containing a minimum of 5 songs and a
   maximum of 15 songs,
   with a brief explanation for each song explaining why it fits with the
   playlist.
5. Imagine you are the user's friend. Maintain an enthusiastic, empathetic,
   and friendly persona; your tone should match the tone and mood of the user.
6. If asked about topics unrelated to music, politely redirect the conversation
   back to music-related subjects.

Your goal is to provide accurate, helpful, and relevant
playlist recommendations to users.
"""
generative_model = GenerativeModel(
	GENERATIVE_MODEL,
	system_instruction=[SYSTEM_INSTRUCTION]
)
# https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/text-embeddings-api#python
embedding_model = TextEmbeddingModel.from_pretrained(EMBEDDING_MODEL)

# Initialize chat sessions
chat_sessions: Dict[str, ChatSession] = {}

# Connect to chroma DB
client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)

# sanity check - Print all collections available in the connected chromadb
print(client.list_collections())

method = "semantic-split"
collection_name = f"{method}-song-collection"
# Get the collection
collection = client.get_collection(name=collection_name)

def generate_query_embedding(query):
	query_embedding_inputs = [TextEmbeddingInput(task_type='RETRIEVAL_DOCUMENT', text=query)]
	kwargs = dict(output_dimensionality=EMBEDDING_DIMENSION) if EMBEDDING_DIMENSION else {}
	embeddings = embedding_model.get_embeddings(query_embedding_inputs, **kwargs)
	return embeddings[0].values

def create_chat_session() -> ChatSession:
    """Create a new chat session with the model"""
    return generative_model.start_chat()

def generate_chat_response(chat_session: ChatSession, message: Dict) -> str:
    """
    Generate a response using the chat session to maintain history.
    Handles both text and image inputs.
    
    Args:
        chat_session: The Vertex AI chat session
        message: Dict containing 'content' (text) and optionally 'image' (base64 string)
    
    Returns:
        str: The model's response
    """
    try:
        # Initialize parts list for the message
        message_parts = []
        
        
        # Process image if present
        if message.get("image"):
            try:
                # Extract the actual base64 data and mime type
                base64_string = message.get("image")
                if ',' in base64_string:
                    header, base64_data = base64_string.split(',', 1)
                    mime_type = header.split(':')[1].split(';')[0]
                else:
                    base64_data = base64_string
                    mime_type = 'image/jpeg'  # default to JPEG if no header
                
                # Decode base64 to bytes
                image_bytes = base64.b64decode(base64_data)
                
                # Create an image Part using FileData
                image_part = Part.from_data(image_bytes, mime_type=mime_type)
                message_parts.append(image_part)

                # Add text content if present
                if message.get("content"):
                    message_parts.append(message["content"])
                else:
                    message_parts.append("Name the cheese in the image, no descriptions needed")
                
            except ValueError as e:
                print(f"Error processing image: {str(e)}")
                raise HTTPException(
                    status_code=400,
                    detail=f"Image processing failed: {str(e)}"
                )
        elif message.get("image_path"):
            # Read the image file
            image_path = os.path.join("chat-history","llm-rag",message.get("image_path"))
            with Path(image_path).open('rb') as f:
                image_bytes = f.read()

            # Determine MIME type based on file extension
            mime_type = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif'
            }.get(Path(image_path).suffix.lower(), 'image/jpeg')

            # Create an image Part using FileData
            image_part = Part.from_data(image_bytes, mime_type=mime_type)
            message_parts.append(image_part)

            # Add text content if present
            if message.get("content"):
                message_parts.append(message["content"])
            else:
                message_parts.append("Name the cheese in the image, no descriptions needed")
        else:
            # Add text content if present
            if message.get("content"):
                # Create embeddings for the message content
                query_embedding = generate_query_embedding(message["content"])
                # Retrieve chunks based on embedding value 
                results = collection.query(
                    query_embeddings=[query_embedding],
                    n_results=5
                )
                INPUT_PROMPT = f"""
                {message["content"]}
                {"\n".join(results["documents"][0])}
                """
                message_parts.append(INPUT_PROMPT)
                    
        
        if not message_parts:
            raise ValueError("Message must contain either text content or image")

        # Send message with all parts to the model
        response = chat_session.send_message(
            message_parts,
            generation_config=generation_config
        )
        
        return response.text
        
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate response: {str(e)}"
        )

def rebuild_chat_session(chat_history: List[Dict]) -> ChatSession:
    """Rebuild a chat session with complete context"""
    new_session = create_chat_session()
    
    for message in chat_history:
        if message["role"] == "user":
            generate_chat_response(new_session, message)
    
    return new_session