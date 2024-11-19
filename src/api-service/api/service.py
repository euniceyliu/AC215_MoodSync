from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.routers import llm_rag_chat  # Only using the provided router

# Initialize FastAPI app
app = FastAPI(
    title="API Server",
    description="API",
    version="v1"
)

# Enable CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],  # Allow all origins (adjust in production)
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include the LLM RAG Chat router
app.include_router(llm_rag_chat.router)


# Root endpoint for basic health check
@app.get("/")
async def get_index():
    return {"message": "Welcome to MoodSync"}

