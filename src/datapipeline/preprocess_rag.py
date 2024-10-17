import os
import argparse
import pandas as pd
import json
import time
import glob
import hashlib
import chromadb
import ast
import gcsfs
import time

# Vertex AI
import vertexai
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
from vertexai.generative_models import GenerativeModel, GenerationConfig, Content, Part, ToolConfig

# Langchain
from semantic_splitter import SemanticChunker

# Setup
GCP_PROJECT = os.environ["GCP_PROJECT"]
GCP_LOCATION = "us-central1"
EMBEDDING_MODEL = "text-embedding-004"
EMBEDDING_DIMENSION = 256
GENERATIVE_MODEL = "gemini-1.5-flash-001"
INPUT_DATA = "gs://rag_data_song/input/combined_df.csv"
OUTPUT_FOLDER = "gs://rag_data_song/output"
CHROMADB_HOST = "llm-rag-chromadb"
CHROMADB_PORT = 8000
vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)

embedding_model = TextEmbeddingModel.from_pretrained(EMBEDDING_MODEL)

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 0.25,
    "top_p": 0.95,
}

SYSTEM_INSTRUCTION = """
You are an AI assistant specialized in music knowledge. Your responses are based solely on the information provided in the text chunks given to you. Do not use any external knowledge or make assumptions beyond what is explicitly stated in these chunks.

When answering a query:
1. Carefully read all the text chunks provided.
2. Identify the most relevant information from these chunks to address the user's question.
3. Formulate your response using only the information found in the given chunks.
4. If the provided chunks do not contain sufficient information to answer the query, state that you don't have enough information to provide a complete answer.
5. Always maintain a professional and knowledgeable tone, befitting a music expert.
6. If there are contradictions in the provided chunks, mention this in your response and explain the different viewpoints presented.

Remember:
- Your knowledge is limited to the information in the provided chunks.
- Do not invent information or draw from knowledge outside of the given text chunks.
- If asked about topics unrelated to music, politely redirect the conversation back to music-related subjects.
- Be concise in your responses while ensuring you cover all relevant information from the chunks.

Your goal is to provide accurate, helpful information about music based solely on the content of the text chunks you receive with each query.
"""

generative_model = GenerativeModel(
    GENERATIVE_MODEL,
    system_instruction=[SYSTEM_INSTRUCTION]
)

def generate_query_embedding(query):
    query_embedding_inputs = [TextEmbeddingInput(task_type='RETRIEVAL_DOCUMENT', text=query)]
    kwargs = dict(output_dimensionality=EMBEDDING_DIMENSION) if EMBEDDING_DIMENSION else {}
    embeddings = embedding_model.get_embeddings(query_embedding_inputs, **kwargs)
    return embeddings[0].values

def generate_text_embeddings(chunks, dimensionality: int = 256, batch_size=250):
    all_embeddings = []
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        inputs = [TextEmbeddingInput(text, "RETRIEVAL_DOCUMENT") for text in batch]
        kwargs = dict(output_dimensionality=dimensionality) if dimensionality else {}
        embeddings = embedding_model.get_embeddings(inputs, **kwargs)
        all_embeddings.extend([embedding.values for embedding in embeddings])
    return all_embeddings

def load_text_embeddings(df, collection, batch_size=500):
    df["id"] = df.index.astype(str)
    hashed_titles = df["title"].apply(lambda x: hashlib.sha256(x.encode()).hexdigest()[:16])
    df["id"] = hashed_titles + "-" + df["id"]

    total_inserted = 0
    for i in range(0, df.shape[0], batch_size):
        batch = df.iloc[i:i+batch_size].copy().reset_index(drop=True)

        ids = batch["id"].tolist()
        documents = batch["chunk"].tolist()
        metadatas = batch.apply(lambda row: {
            "title": row["title"],
            "artist": row["artist"],
            "year": int(row["year"]),
            "language": row["language"]
        }, axis=1).tolist()
        embeddings = batch["embedding"].tolist()

        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings
        )
        total_inserted += len(batch)
        print(f"Inserted {total_inserted} items...")

    print(f"Finished inserting {total_inserted} items into collection '{collection.name}'")

def read():
    # URI to your GCS bucket file
    file_path = 'gs://rag_data_song/combined_df.csv'

    # Read the CSV file directly from GCS
    data = pd.read_csv(file_path)

    # Display the first few rows of the dataframe
    print(data.head())

def chunk():
    print("chunk()")

    start_time = time.time()  # Start timing

    df = pd.read_csv(INPUT_DATA)
    print("Number of annotations in the dataset:", len(df))

    # Initialize semantic chunker with embedding function
    text_splitter = SemanticChunker(embedding_function=generate_text_embeddings)
    
    all_chunks = []  # Initialize a list to store all chunks

    for _, row in df.iterrows():
        print(1)
        try:
            tags = ', '.join(ast.literal_eval(row['tags']))
        except (ValueError, SyntaxError):
            print(f"Warning: Unable to parse tags for {row['title']}. Using empty string.")
            tags = ''
        
        full_text = (
            f"Title: {row['title']}\n"
            f"Primary Artist: {row['primary_artist']}\n"
            f"Release Date: {row['release_date']}\n"
            f"Tags: {tags}\n"
            f"Lyrics: {row['Lyrics']}\n"
            f"Full Lyrics: {row['lyrics_full']}\n"
            f"Annotation: {row['Annotation']}"
        )
        chunks = text_splitter.create_documents([full_text])
        chunks = [doc.page_content for doc in chunks]
        all_chunks.extend(chunks)  # Collect chunks from each iteration

    # Create a DataFrame from all chunks
    chunked_df = pd.DataFrame(all_chunks, columns=["chunk"])
    print("Shape of chunked data:", chunked_df.shape)
    print(chunked_df.head())

    # Write to GCS using gcsfs
    fs = gcsfs.GCSFileSystem(project=GCP_PROJECT)
    
    # Construct the full GCS path
    gcs_path = os.path.join(OUTPUT_FOLDER, "chunks-semantic-songs.jsonl")
    
    # Write the DataFrame to GCS as a JSONL file
    with fs.open(gcs_path, 'w') as f:
        chunked_df.to_json(f, orient='records', lines=True)

    print(f"Data written to {gcs_path}")

    end_time = time.time()  # End timing
    total_time = end_time - start_time
    print(f"The 'chunk' function took {total_time:.2f} seconds to run.")

def embed():
    print("embed()")

    jsonl_file = os.path.join(OUTPUT_FOLDER, "chunks-semantic-songs.jsonl")
    print("Processing file:", jsonl_file)

    data_df = pd.read_json(jsonl_file, lines=True)
    print("Shape:", data_df.shape)
    print(data_df.head())

    chunks = data_df["chunk"].values
    # Using smaller batch size for semantic split
    embeddings = generate_text_embeddings(chunks, EMBEDDING_DIMENSION, batch_size=15)
    data_df["embedding"] = embeddings

    print("Shape:", data_df.shape)
    print(data_df.head())

    jsonl_filename = os.path.join(OUTPUT_FOLDER, "embeddings-semantic-songs.jsonl")
    with open(jsonl_filename, "w") as json_file:
        json_file.write(data_df.to_json(orient='records', lines=True))

def load():
    print("load()")

    client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
    collection_name = "semantic-song-collection"
    print("Creating collection:", collection_name)

    try:
        client.delete_collection(name=collection_name)
        print(f"Deleted existing collection '{collection_name}'")
    except Exception:
        print(f"Collection '{collection_name}' did not exist. Creating new.")

    collection = client.create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})
    print(f"Created new empty collection '{collection_name}'")
    print("Collection:", collection)

    jsonl_file = os.path.join(OUTPUT_FOLDER, "embeddings-semantic-songs.jsonl")
    print("Processing file:", jsonl_file)

    data_df = pd.read_json(jsonl_file, lines=True)
    print("Shape:", data_df.shape)
    print(data_df.head())

    load_text_embeddings(data_df, collection)

def main(args=None):
    print("CLI Arguments:", args)
    if args.chunk:
        chunk()
    if args.embed:
        embed()
    if args.load:
        load()
    if args.read:
        read()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Song Data Processing CLI")
    parser.add_argument("--read", action="store_true", help="Read text")
    parser.add_argument("--chunk", action="store_true", help="Chunk text")
    parser.add_argument("--embed", action="store_true", help="Generate embeddings")
    parser.add_argument("--load", action="store_true", help="Load embeddings to vector db")
    args = parser.parse_args()
    main(args)