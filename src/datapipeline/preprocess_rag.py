
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
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
# Setup
GCP_PROJECT = os.environ["GCP_PROJECT"]
GCP_LOCATION = "us-central1"
EMBEDDING_MODEL = "text-embedding-004"
EMBEDDING_DIMENSION = 256
GENERATIVE_MODEL = "gemini-1.5-flash-001"
# use test dataset for now
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
    """Generate embeddings for text chunks, trimming those that exceed token limits."""
    all_embeddings = []
    MAX_CHARS = 60000  # Approximate character limit corresponding to 20k tokens

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        
        # Trim any chunks that are too long
        processed_batch = [text[:MAX_CHARS] if len(text) > MAX_CHARS else text for text in batch]
        
        inputs = [TextEmbeddingInput(text, "RETRIEVAL_DOCUMENT") for text in processed_batch]
        kwargs = dict(output_dimensionality=dimensionality) if dimensionality else {}
        
        try:
            embeddings = embedding_model.get_embeddings(inputs, **kwargs)
            all_embeddings.extend([embedding.values for embedding in embeddings])
        except Exception as e:
            print(f"Error processing batch {i}-{i+batch_size}: {str(e)}")
            # Process one at a time if batch fails
            for text in processed_batch:
                try:
                    single_input = [TextEmbeddingInput(text, "RETRIEVAL_DOCUMENT")]
                    embedding = embedding_model.get_embeddings(single_input, **kwargs)
                    all_embeddings.append(embedding[0].values)
                except Exception as e:
                    print(f"Error processing individual text: {str(e)}")
                    # Add zeros for failed embeddings
                    all_embeddings.append([0.0] * dimensionality)
    
    return all_embeddings

def load_text_embeddings(df, collection, batch_size=500):
    """Load text embeddings into ChromaDB with preserved metadata"""
    df["id"] = df.index.astype(str)
    hashed_titles = df["title"].apply(lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:16])
    df["id"] = hashed_titles + "-" + df["id"]

    total_inserted = 0
    for i in range(0, df.shape[0], batch_size):
        batch = df.iloc[i:i+batch_size].copy().reset_index(drop=True)

        ids = batch["id"].tolist()
        documents = batch["chunk"].tolist()
        
        # Use the metadata fields directly from the DataFrame
        metadatas = batch.apply(lambda row: {
            "title": str(row["title"]),
            "primary_artist": str(row["primary_artist"]),
            "release_date": str(row["release_date"]),
            "tags": str(row["tags"])
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

def chunk(method="semantic-split"):
    print(f"chunk() using method: {method}")
    start_time = time.time()

    df = pd.read_csv(INPUT_DATA)
    print("Number of annotations in the dataset:", len(df))

    chunked_data = []  # Initialize a list to store all chunks

    # Initialize the appropriate text splitter based on method
    if method == "char-split":
        chunk_size = 350
        chunk_overlap = 20
        text_splitter = CharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap, 
            separator='', 
            strip_whitespace=False
        )
    elif method == "recursive-split":
        chunk_size = 350
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size)
    elif method == "semantic-split":
        text_splitter = SemanticChunker(embedding_function=generate_text_embeddings)
    else:
        raise ValueError(f"Unknown chunking method: {method}")

    for i, (_, row) in enumerate(df.iterrows()):
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
            f"Annotation: {row['Annotation']}\n"
        )

        chunks = text_splitter.create_documents([full_text])
        
        chunks = [doc.page_content for doc in chunks]

        # Append each chunk to the list
        for chunk in chunks:
            chunked_data.append({
                "chunk": chunk,
                "title": row['title'],
                "primary_artist": row['primary_artist'],
                "release_date": row['release_date'],
                "tags": tags  # Fixed syntax error: changed "tag:" to "tags"
            })
        
        if i % 1000 == 0:
            print(f"Processed {i} rows")
        
    # Create a DataFrame from the list of dictionaries
    chunked_df = pd.DataFrame(chunked_data)
    print("Shape of chunked data:", chunked_df.shape)
    print(chunked_df.head())

    # Create a DataFrame from all chunks
    # chunked_df = pd.DataFrame(all_chunks, columns=["chunk"])
    print("Shape of chunked data:", chunked_df.shape)
    print(chunked_df.head())

    # Write to GCS using gcsfs
    fs = gcsfs.GCSFileSystem(project=GCP_PROJECT)
    gcs_path = os.path.join(OUTPUT_FOLDER, f"chunks-{method}-songs.jsonl")
    
    with fs.open(gcs_path, 'w') as f:
        chunked_df.to_json(f, orient='records', lines=True)

    print(f"Data written to {gcs_path}")

    end_time = time.time()
    total_time = end_time - start_time
    print(f"The 'chunk' function took {total_time:.2f} seconds to run.")

def embed(method="semantic-split"):
    print(f"embed() using method: {method}")
    start_time = time.time()

    jsonl_file = os.path.join(OUTPUT_FOLDER, f"chunks-{method}-songs.jsonl")
    print("Processing file:", jsonl_file)

    data_df = pd.read_json(jsonl_file, lines=True)
    print("Shape:", data_df.shape)
    print(data_df.head())

    # Filter out empty chunks
    data_df = data_df[data_df['chunk'].notna() & (data_df['chunk'].str.strip() != '')]
    print(f"Shape after removing empty chunks: {data_df.shape}")

    chunks = data_df["chunk"].values

    # Adjust batch size based on method
    batch_size = 15 if method == "semantic-split" else 100
    embeddings = generate_text_embeddings(chunks, EMBEDDING_DIMENSION, batch_size=batch_size)
    data_df["embedding"] = embeddings

    print("Shape:", data_df.shape)
    print(data_df.head())

    fs = gcsfs.GCSFileSystem(project=GCP_PROJECT)
    gcs_path = os.path.join(OUTPUT_FOLDER, f"embeddings-{method}-songs.jsonl")
    
    with fs.open(gcs_path, 'w') as f:
        data_df.to_json(f, orient='records', lines=True)

    end_time = time.time()
    total_time = end_time - start_time
    print(f"The 'embed' function took {total_time:.2f} seconds to run.")

def load(method="semantic-split"):
    print(f"load() using method: {method}")

    client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
    collection_name = f"{method}-song-collection"
    print("Creating collection:", collection_name)

    try:
        client.delete_collection(name=collection_name)
        print(f"Deleted existing collection '{collection_name}'")
    except Exception:
        print(f"Collection '{collection_name}' did not exist. Creating new.")

    collection = client.create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})
    print(f"Created new empty collection '{collection_name}'")
    print("Collection:", collection)

    jsonl_file = os.path.join(OUTPUT_FOLDER, f"embeddings-{method}-songs.jsonl")
    print("Processing file:", jsonl_file)

    data_df = pd.read_json(jsonl_file, lines=True)
    print("Shape:", data_df.shape)
    print(data_df.head())

    load_text_embeddings(data_df, collection)

def query(method="semantic-split"):
    print("query()")

    # Connect to chroma DB
    client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)

    # Get collection
    collection_name = f"{method}-song-collection"

    query = "I need a chill playlist for studying with ambient and lo-fi beats to help me focus."
    query_embedding = generate_query_embedding(query)
    print("Embedding values:", query_embedding)

    # Get the collection
    collection = client.get_collection(name=collection_name)

    # 1: Basic similarity search
    print("\n1. Basic Similarity Search:")
    print("Query:", query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        include=['documents', 'metadatas', 'distances']  # Include all available information
    )
    print_results(results)

    # 2: Query with artist filter
    print("\n2. Query with Artist Filter: Kendrick-lamar")
    artist_results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        where={"primary_artist": "Kendrick-lamar"},
        include=['documents', 'metadatas', 'distances']
    )
    print_results(artist_results)

    # 3: Query with lexical search
    print("\n3. Query with Lexical Search: contains reminising")
    lexical_results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        where_document={"$contains": "reminising"},
        include=['documents', 'metadatas', 'distances']
    )
    print_results(lexical_results)

def print_results(results):
    """Helper function to print query results in a formatted way"""
    if not results or not results['ids']:
        print("No results found")
        return
    
    print(f"\nFound {len(results['ids'][0])} results:")
    
    for i in range(len(results['ids'][0])):
        print(f"\nResult {i + 1}:")
        print(f"ID: {results['ids'][0][i]}")
        if 'documents' in results and results['documents']:
            print(f"Document: {results['documents'][0][i][:200]}...")  # Print first 200 chars
        if 'metadatas' in results and results['metadatas']:
            print(f"Metadata: {results['metadatas'][0][i]}")
        if 'distances' in results and results['distances']:
            print(f"Distance: {results['distances'][0][i]}")
        print("-" * 80)

def main(args=None):
    print("CLI Arguments:", args)
    if args.chunk:
        chunk(method=args.chunk_type)
    if args.embed:
        embed(method=args.chunk_type)
    if args.load:
        load(method=args.chunk_type)
    if args.read:
        read()
    if args.query:
        query(method=args.chunk_type)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Song Data Processing CLI")
    parser.add_argument("--read", action="store_true", help="Read text")
    parser.add_argument("--chunk", action="store_true", help="Chunk text")
    parser.add_argument("--embed", action="store_true", help="Generate embeddings")
    parser.add_argument("--load", action="store_true", help="Load embeddings to vector db")
    parser.add_argument(
		"--query",
		action="store_true",
		help="Query vector db",
	)
    parser.add_argument(
        "--chunk_type", 
        default="semantic-split", 
        choices=["char-split", "recursive-split", "semantic-split"],
        help="Chunking method to use"
    )
    args = parser.parse_args()
    main(args)