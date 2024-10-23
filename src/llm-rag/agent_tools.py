import json
import vertexai
from vertexai.generative_models import FunctionDeclaration, Tool, Part

# Specify a function declaration and parameters for an API request
get_chunk_by_artist_func = FunctionDeclaration(
    name="get_chunk_by_artist",
    description="Get the chunks filtered by artist name",
    # Function parameters are specified in OpenAPI JSON schema format
    parameters={
        "type": "object",
        "properties": {
            "artist": {"type": "string", "description": "The artist name","enum":["Zedd", "Future", "Selena-gomez", "Jay-z", "Beyonce"]},
            "search_content": {"type": "string", "description": "The search text to filter content from lyric annotations. The search term is compared against the song text based on cosine similarity. Expand the search term to a a sentence or two to get better matches"},
        },
        "required": ["artist","search_content"],
    },
)

def get_chunk_by_artist(artist, search_content, collection, embed_func):

    query_embedding = embed_func(search_content)

    # Query based on embedding value 
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,# can change this depending on how many chunks we expect to be relevant
        where={"primary_artist": artist}
    )
    results_string = ""
    for i in range(len(results['ids'][0])):
        results_string += str(results['metadatas'][0][i])
        results_string += results['documents'][0][i]
        results_string += '\n'
    
    return results_string



# Define all functions available to the cheese expert
music_expert_tool = Tool(function_declarations=[get_chunk_by_artist_func])


def execute_function_calls(function_calls,collection, embed_func):
    parts = []
    for function_call in function_calls:
        print("Function:",function_call.name)
        if function_call.name == "get_chunk_by_artist":
            print("Calling function with args:", function_call.args["artist"], function_call.args["search_content"])
            response = get_chunk_by_artist(function_call.args["artist"], function_call.args["search_content"],collection, embed_func)
            print("Response:", response)
            #function_responses.append({"function_name":function_call.name, "response": response})
            parts.append(
					Part.from_function_response(
						name=function_call.name,
						response={
							"content": response,
						},
					),
			)

    
    return parts
