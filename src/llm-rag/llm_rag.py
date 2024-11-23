import os
import argparse
import pandas as pd
import hashlib
import chromadb

# Vertex AI
import vertexai
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
from vertexai.generative_models import (
    GenerativeModel,
    GenerationConfig,
    Content,
    Part,
    ToolConfig,
)

import agent_tools


# Setup
GCP_PROJECT = "ac215-project-438523"
GCP_LOCATION = "us-central1"
EMBEDDING_MODEL = "text-embedding-004"
EMBEDDING_DIMENSION = 256
GENERATIVE_MODEL = "gemini-1.5-flash-002"
# use test dataset for now
INPUT_DATA = "gs://rag_data_song/input/combined_df_test.csv"
OUTPUT_FOLDER = "gs://rag_data_song/output"
CHROMADB_HOST = "llm-rag-chromadb-chat"
CHROMADB_PORT = 8000
vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)

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

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 0.5,
    "top_p": 0.95,
}


MODEL_ENDPOINT = (
    "projects/473040659708/locations/us-central1/"
    "endpoints/1976395240671543296"
)
finetuned_model = GenerativeModel(
    MODEL_ENDPOINT, system_instruction=[SYSTEM_INSTRUCTION]
)


def generate_query_embedding(query):
    embedding_model = TextEmbeddingModel.from_pretrained(EMBEDDING_MODEL)
    query_embedding_inputs = [
        TextEmbeddingInput(task_type="RETRIEVAL_DOCUMENT", text=query)
    ]
    kwargs = (
        dict(output_dimensionality=EMBEDDING_DIMENSION)
        if EMBEDDING_DIMENSION
        else {}
    )
    embeddings = embedding_model.get_embeddings(
        query_embedding_inputs, **kwargs
    )
    return embeddings[0].values


def load_text_embeddings(df, collection, batch_size=500):
    """Load text embeddings into ChromaDB with preserved metadata"""
    df["id"] = df.index.astype(str)
    hashed_titles = df["title"].apply(
        lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:16]
    )
    df["id"] = hashed_titles + "-" + df["id"]

    total_inserted = 0
    for i in range(0, df.shape[0], batch_size):
        batch = df.iloc[i: i + batch_size].copy().reset_index(drop=True)

        ids = batch["id"].tolist()
        documents = batch["chunk"].tolist()

        # Use the metadata fields directly from the DataFrame
        metadatas = batch.apply(
            lambda row: {
                "title": str(row["title"]),
                "primary_artist": str(row["primary_artist"]),
                "release_date": str(row["release_date"]),
                "tags": str(row["tags"]),
            },
            axis=1,
        ).tolist()

        embeddings = batch["embedding"].tolist()

        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
        )
        total_inserted += len(batch)
        print(f"Inserted {total_inserted} items...")

    print(
        f"Finished inserting {total_inserted} items into "
        f"collection '{collection.name}'"
    )


def load(method="semantic-split-full-lyrics"):
    print(f"load() using method: {method}")

    client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
    collection_name = f"{method}-song-collection"
    print("Creating collection:", collection_name)

    try:
        client.delete_collection(name=collection_name)
        print(f"Deleted existing collection '{collection_name}'")
    except Exception:
        print(f"Collection '{collection_name}' did not exist. Creating new.")

    collection = client.create_collection(
        name=collection_name, metadata={"hnsw:space": "cosine"}
    )
    print(f"Created new empty collection '{collection_name}'")
    print("Collection:", collection)

    jsonl_file = os.path.join(OUTPUT_FOLDER, f"embeddings-{method}.jsonl")
    print("Processing file:", jsonl_file)

    data_df = pd.read_json(jsonl_file, lines=True)
    print("Shape:", data_df.shape)
    print(data_df.head())

    load_text_embeddings(data_df, collection)


def print_results(results):
    """Helper function to print query results in a formatted way"""
    if not results or not results["ids"]:
        print("No results found")
        return

    print(f"\nFound {len(results['ids'][0])} results:")

    for i in range(len(results["ids"][0])):
        print(f"\nResult {i + 1}:")
        print(f"ID: {results['ids'][0][i]}")
        if "documents" in results and results["documents"]:
            print(
                f"Document: {results['documents'][0][i][:200]}..."
            )  # Print first 200 chars
        if "metadatas" in results and results["metadatas"]:
            print(f"Metadata: {results['metadatas'][0][i]}")
        if "distances" in results and results["distances"]:
            print(f"Distance: {results['distances'][0][i]}")
        print("-" * 80)


def query(method="semantic-split-full-lyrics"):
    print("query()")

    # Connect to chroma DB
    client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)

    # Get collection
    collection_name = f"{method}-song-collection"

    query = """love song"""
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
        include=[
            "documents",
            "metadatas",
            "distances",
        ],  # Include all available information
    )
    print_results(results)

    # 2: Query with artist filter
    print("\n2. Query with Artist Filter: Kendrick-lamar")
    artist_results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        where={"primary_artist": "Kendrick-lamar"},
        include=["documents", "metadatas", "distances"],
    )
    print_results(artist_results)

    # 3: Query with lexical search
    print("\n3. Query with Lexical Search:")
    lexical_results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        where_document={"$contains": "beach"},
        include=["documents", "metadatas", "distances"],
    )
    print_results(lexical_results)


def chat(method="semantic-split-full-lyrics"):
    print("chat()")

    generative_model = GenerativeModel(
        GENERATIVE_MODEL, system_instruction=[SYSTEM_INSTRUCTION]
    )
    # Connect to chroma DB
    client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
    # Get a collection object from an existing collection
    collection_name = f"{method}-song-collection"

    query = """sad"""
    query_embedding = generate_query_embedding(query)
    print("Query:", query)
    # Get the collection
    collection = client.get_collection(name=collection_name)

    # Query based on embedding value
    results = collection.query(query_embeddings=[query_embedding], n_results=5)

    print("\n\nResults:", results)

    results_string = ""

    for i in range(len(results["ids"][0])):
        # results_string += str(results['metadatas'][0][i])
        results_string += results["documents"][0][i]
        results_string += "\n"

    INPUT_PROMPT = f"""{query}{results_string}"""

    print("INPUT_PROMPT: ", INPUT_PROMPT)
    response = generative_model.generate_content(
        [INPUT_PROMPT],  # Input prompt
        generation_config=generation_config,  # Configuration settings
        stream=False,  # Enable streaming for responses
    )
    generated_text = response.text
    print("LLM Response:", generated_text)
    return generated_text


def agent(query, method="semantic-split-full-lyrics"):
    print("agent()")
    generative_model = GenerativeModel(
        GENERATIVE_MODEL, system_instruction=[SYSTEM_INSTRUCTION]
    )
    # Connect to chroma DB
    client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
    # Get a collection object from an existing collection
    collection_name = f"{method}-song-collection"
    # Get the collection
    collection = client.get_collection(name=collection_name)

    # User prompt
    user_prompt_content = Content(
        role="user",
        parts=[
            Part.from_text(
                query
            )
        ],
    )

    # Step 1: Prompt LLM to find the tool(s) to execute
    print("user_prompt_content: ", user_prompt_content)
    response = generative_model.generate_content(
        user_prompt_content,
        generation_config=GenerationConfig(
            temperature=0
        ),  # Configuration settings
        tools=[agent_tools.music_expert_tool],  # Tools available to the model
        tool_config=ToolConfig(
            function_calling_config=ToolConfig.FunctionCallingConfig(
                # ANY mode forces the model to predict only function calls
                mode=ToolConfig.FunctionCallingConfig.Mode.ANY,
            )
        ),
    )
    print("LLM Response:", response)

    # Step 2: Execute the function and send chunks back to LLM to answer
    function_calls = response.candidates[0].function_calls
    print("Function calls:")
    function_responses = agent_tools.execute_function_calls(
        function_calls, collection, embed_func=generate_query_embedding
    )
    if len(function_responses) == 0:
        print("Function calls did not result in any responses...")
    else:
        # Call finetuned LLM with retrieved responses
        response = finetuned_model.generate_content(
            [
                user_prompt_content,  # User prompt
                response.candidates[0].content,  # Function call response
                Content(parts=function_responses),
            ],
            tools=[agent_tools.music_expert_tool],
        )
        print("LLM Response:", response)


def main(args=None):
    print("CLI Arguments:", args)
    if args.load:
        load(method=args.chunk_type)
    if args.query:
        query(method=args.chunk_type)
    if args.chat:
        chat(method=args.chunk_type)
    if args.agent:
        agent(query=args.querymessage, method=args.chunk_type)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Song Data Processing CLI")
    parser.add_argument(
        "--load", action="store_true", help="Load embeddings to vector db"
    )
    parser.add_argument(
        "--query",
        action="store_true",
        help="Query vector db",
    )
    parser.add_argument(
        "--querymessage",
        type=str,
        help="Message to query"
    )
    parser.add_argument(
        "--chunk_type",
        default="semantic-split-full-lyrics",
        choices=[
            "char-split",
            "recursive-split",
            "semantic-split",
            "char-split-full-lyrics",
            "semantic-split-full-lyrics",
            "char-split-annotation-only",
        ],
        help="Chunking method to use",
    )
    parser.add_argument(
        "--chat",
        action="store_true",
        help="Chat with LLM",
    )

    parser.add_argument(
        "--agent",
        action="store_true",
        help="Chat with LLM Agent",
    )

    args = parser.parse_args()
    main(args)
