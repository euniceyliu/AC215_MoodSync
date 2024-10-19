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
INPUT_DATA = "gs://rag_data_song/input/combined_df_test.csv"
OUTPUT_FOLDER = "gs://rag_data_song/output"
CHROMADB_HOST = "llm-rag-chromadb-chat"
CHROMADB_PORT = 8000
vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)

embedding_model = TextEmbeddingModel.from_pretrained(EMBEDDING_MODEL)


### good for chat
SYSTEM_INSTRUCTION = """
You are an AI assistant specialized in music knowledge. 
Your goal is to recommend personalized music playlists based on the user's input. 
Following the users' input, there will also be some chunks of data that might be a little relevant and inform you to make better recommendations.

When answering a query:
1. Carefully read all the text chunks provided.
2. Consider the user's mood, interests, and personal music preferences to craft the perfect playlist for them
3. Select the most appropriate song given the state of the user from their text input.
4. Always maintain a professional and knowledgeable tone, befitting a music expert.

Remember:
- Do not invent information, or hallucinate.
- If asked about topics unrelated to music, politely redirect the conversation back to music-related subjects.
- Be concise in your responses while ensuring you cover all relevant information from the chunks.

Your goal is to provide accurate, helpful, and relevant playlist recommendations to users.
"""
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 0.01,
    "top_p": 0.95,
}



### good for query 
"""
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
"""
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 0.25,
    "top_p": 0.95,
}
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

    query = f"""
    pre-game energy, something that keeps the crew lit but not too wild, we like edm
    """
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



#flatten metadata
def extract_strings(item):
    if isinstance(item, dict):
        # Extract string values from the dictionary (adjust as needed)
        return " ".join(str(v) for v in item.values())
    elif isinstance(item, list):
        # Recursively flatten lists and extract strings
        return " ".join(map(extract_strings, item))
    else:
        # Convert non-string items to strings directly
        return str(item)


def chat(method="semantic-split"):
	print("chat()")

	# Connect to chroma DB
	client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
	# Get a collection object from an existing collection, by name. If it doesn't exist, create it.
	collection_name = f"{method}-song-collection"

	query = f"""
            I need a chill playlist for studying with ambient and lo-fi beats to help me focus.
            """
	query_embedding = generate_query_embedding(query)
	print("Query:", query)
	#print("Embedding values:", query_embedding)
	# Get the collection
	collection = client.get_collection(name=collection_name)

	# Query based on embedding value 
	results = collection.query(
		query_embeddings=[query_embedding],
		n_results=1
	)
	print("\n\nResults:", results)
	#print(len(results["documents"][0]))

    #     {"below are some related context that might help you choose better playlists:"}
    #chr(10) is \n for f-string
	INPUT_PROMPT = f"""
	{query}
	{chr(10).join(results["documents"][0])}
    {"".join("".join(extract_strings(results["metadatas"][0])))}
	"""
    #    {"".join("".join(extract_strings(results["metadatas"][0])))}
    #probably need a way to combine the different keys of the same entry from the results dict

	print("INPUT_PROMPT: ",INPUT_PROMPT)
	response = generative_model.generate_content(
		[INPUT_PROMPT],  # Input prompt
		generation_config=generation_config,  # Configuration settings
		stream=False,  # Enable streaming for responses
	)
	generated_text = response.text
	print("LLM Response:", generated_text)


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
    if args.load:
        load(method=args.chunk_type)
    if args.query:
        query(method=args.chunk_type)
    if args.chat:
        chat(method=args.chunk_type)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Song Data Processing CLI")
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
    parser.add_argument(
		"--chat",
		action="store_true",
		help="Chat with LLM",
	)
    args = parser.parse_args()
    main(args)