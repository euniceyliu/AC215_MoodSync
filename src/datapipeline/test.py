import os
import requests
GCP_PROJECT = os.environ["GCP_PROJECT"]
GCP_LOCATION = "us-central1"
EMBEDDING_MODEL = "text-embedding-004"
EMBEDDING_DIMENSION = 256
GENERATIVE_MODEL = "gemini-1.5-flash-001"
# use test dataset for now
INPUT_DATA = "gs://rag_data_song/input/combined_df_test.csv"
OUTPUT_FOLDER = "gs://rag_data_song/output"
CHROMADB_HOST = "llm-rag-chromadb"
CHROMADB_PORT = 8000
try:
    response = requests.get(f"{CHROMADB_HOST}:{CHROMADB_PORT}/tenants/")
    print("Response from ChromaDB:", response.json())
except Exception as e:
    print("Error connecting to ChromaDB:", e)

