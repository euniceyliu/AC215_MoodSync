import os
import argparse
import pandas as pd
import json
import time
import glob
import csv
from google.cloud import storage
import glob
from sklearn.model_selection import train_test_split
import vertexai
from vertexai.preview.tuning import sft
from vertexai.generative_models import GenerativeModel, GenerationConfig, SafetySetting

# Setup
GCP_PROJECT = os.environ["GCP_PROJECT"]
GCS_BUCKET_NAME = 'prompt-playlist-data'
GCP_LOCATION = "us-central1"
GENERATIVE_SOURCE_MODEL = "gemini-1.5-flash-002" # gemini-1.5-pro-002
# Configuration settings for the content generation
generation_config = {
    "max_output_tokens": 3000,  # Maximum number of tokens for output
    "temperature": 0.75,  # Control randomness in output
    "top_p": 0.95,  # Use nucleus sampling
}

# Safety settings to filter out harmful content
safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    )
]

FILENAME = "prompt_playlist_data.txt"

SYSTEM_INSTRUCTION = """Here is a playlist of songs with the playlist title and description. Using information from
the title, description, and playlist content, generate a natural language prompt that a user might input into an AI 
playlist generator to obtain the playlist of interest. You do not have to have to use the exact wording in the title/description,
but use the information to infer the underlying context/emotion to generate a unique prompt. The prompt must follow least one of the following guidelines:
1. Use modern day slang words such as 'sauce', 'slap', 'fire', 'wavy'.
2. Do not explicitly ask for a playlist, but rather just state the user's current context or mood, such as 'Today has been a long day.'
3. Provides an abstract but human feeling, such as 'Give me a playlist that feels like driving down an empty road at 2 AM with no destination in mind.'
4. You may make up reasonable details to include in the prompt if the title/description are not informative enough.

Next, assume you are an expert at recommending personalized playlists. Embed the provided playlist recommendation in natural language with the following guidelines:
1. Acknowledge that you understand the user's needs and their emotions. Use an empathetic and enthusiastic tone. 
2. Cater to the tone of the user. For example, if they use slang, you can speak conversationally and casual. If they are sad, use a gentle and comforting tone.
3. Present a maximum of 15 songs in the playlist, and provide a brief explanation as to why each song is included in the playlist.

Output Format:
Provide the Prompt and Response pairs in the following format:
{"prompt": "I'm feeling lost.","response": "I'm really sorry you're feeling lost right now. That can be such a tough and confusing place to be. Let me create a playlist that gives you some space to reflect, with calming, grounding tracks and a few uplifting ones that gently remind you you're not alone.\n**Holocene – Bon Iver** A hauntingly beautiful song that captures feelings of introspection and searching for meaning.\n**Lost in the Light – Bahamas** A mellow, soothing track that feels like a gentle reminder that it's okay to not have everything figured out.\n**River – Leon Bridges** A soulful and calming song about seeking peace and redemption.  I hope these tracks bring you a sense of comfort and help you navigate through the emotions you're experiencing."},
"""

vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)


def generate_data(file_path):
    df = pd.read_csv(file_path)
    generative_model = GenerativeModel(
        GENERATIVE_SOURCE_MODEL,
        system_instruction = [SYSTEM_INSTRUCTION]
    )
    for index, row in df.iterrows():
        songs = row['songs']
        title = row['title']
        description = row['description']
        query = f"Playlist Title: {title}, Description: {description}, Songs: {songs}"
        time.sleep(2)
        response = generative_model.generate_content(
            [query],  # Input prompt
            generation_config=generation_config,  # Configuration settings
            stream=False  # Enable streaming for responses
            )
        generated_text = response.text
        print('Writing data file...')
        with open(FILENAME, "a") as file:
            file.write(generated_text)


def prepare():
    with open(FILENAME, "r") as read_file:
        text_response = read_file.read()
        text_response = text_response.replace("```\n```json",",").replace("```json","").replace("```", "")
        text_response = '['+text_response+']'
        json_response = json.loads(text_response)
        final_df = pd.DataFrame(json_response)
        final_df.to_csv('finetune_df.csv', index=False)
        final_df["contents"] = final_df.apply(lambda row: [{"role":"user","parts":[{"text": row["prompt"]}]},{"role":"model","parts":[{"text": row["response"]}]}], axis=1)
        df_train, df_test = train_test_split(final_df, test_size=0.1, random_state=42)
        with open("train.jsonl", "w") as json_file:
            json_file.write(df_train[["contents"]].to_json(orient='records', lines=True))
        with open("test.jsonl", "w") as json_file:
            json_file.write(df_test[["contents"]].to_json(orient='records', lines=True))
        with open("data_generating_prompt.txt", "w") as file:
            file.write(SYSTEM_INSTRUCTION)


def upload(version):
    print("upload()")

    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    timeout = 300

    data_files = glob.glob("*.jsonl") + glob.glob("*.csv") + glob.glob("*.txt")
    data_files.sort()
    
    # Upload data
    for index, data_file in enumerate(data_files):
        destination_blob_name = os.path.join(version, data_file)
        blob = bucket.blob(destination_blob_name)
        print("Uploading file:", data_file, destination_blob_name)
        blob.upload_from_filename(data_file, timeout=timeout)

def main(args=None):
    print("CLI Arguments:", args)

    if args.prepare:
        prepare()
    
    if args.generate_data:
        generate_data(args.file)

    if args.upload:
        upload(args.version)


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal '--help', it will provide the description
    parser = argparse.ArgumentParser(description="CLI")

    parser.add_argument(
        "--generate_data",
        action="store_true",
        help="Generate fine-tuning data",
    )

    parser.add_argument('--file', 
        type=str, 
        help="Path to the CSV file for generating data.")

    parser.add_argument(
        "--prepare",
        action="store_true",
        help="Prepare data",
    )
    parser.add_argument(
        "--upload",
        action="store_true",
        help="Upload data to GCS"
    )

    parser.add_argument('--version',
    type=str,
    help="Specify version of data to upload")


    args = parser.parse_args()

    main(args)
