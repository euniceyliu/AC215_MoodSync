import os
import argparse
import pandas as pd
import json
import time
import glob
from google.cloud import storage
import vertexai
from vertexai.preview.tuning import sft
from vertexai.generative_models import GenerativeModel, GenerationConfig, SafetySetting

# Setup
GCP_PROJECT = os.environ["GCP_PROJECT"]
GCP_LOCATION = "us-central1"
GENERATIVE_SOURCE_MODEL = "gemini-1.5-flash-002" # gemini-1.5-pro-002
# Configuration settings for the content generation
generation_config = {
    "max_output_tokens": 5000,  # Maximum number of tokens for output
    "temperature": 1.2,  # Control randomness in output
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

SYSTEM_INSTRUCTION = """You are an expert at generating personalized playlists.
Consider the user's mood, interests, and personal music preferences to craft
the perfect playlist. Match the energy of the user's tone & what they're looking for, i.e. if they are casual, you can use slang;
if they are excited, use exclamations; if they are sad, be comforting."""

vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)
queries = ["I'm feeling pumped on caffeine. Help me chill out with some calming music. I'm into Mac Miller songs", 
        "sunny, beaches, convertible",
        "I have an important exam tomorrow",
        "pre-game energy, something that keeps the crew lit but not too wild, we like edm"]

def foundational_model_chat():
    generative_model = GenerativeModel(
        GENERATIVE_SOURCE_MODEL, 
        system_instruction='You are an expert at generating personalized playlists. Craft the perfect playlist for the user'
    )

    for query in queries:
        print("query: ",query)
        response = generative_model.generate_content(
            [query],  # Input prompt
            generation_config=generation_config,  # Configuration settings
            stream=False,  # Enable streaming for responses
        )
        generated_text = response.text
        print("Foundational LLM Response:", generated_text)

def train(dataversion, wait_for_job=False):
    print("train()")
    TRAIN_DATASET = f"gs://prompt-playlist-data/{dataversion}/train.jsonl" 
    VALIDATION_DATASET = f"gs://prompt-playlist-data/{dataversion}/test.jsonl" 
    # Supervised Fine Tuning
    sft_tuning_job = sft.train(
        source_model=GENERATIVE_SOURCE_MODEL,
        train_dataset=TRAIN_DATASET,
        validation_dataset=VALIDATION_DATASET,
        epochs=15,
        adapter_size=4,
        learning_rate_multiplier=1.0,
        tuned_model_display_name=f"finetuned-model-{dataversion}",
    )
    print("Training job started. Monitoring progress...\n\n")
    
    # Wait and refresh
    time.sleep(60)
    sft_tuning_job.refresh()
    
    if wait_for_job:
        print("Check status of tuning job:")
        print(sft_tuning_job)
        while not sft_tuning_job.has_ended:
            time.sleep(60)
            sft_tuning_job.refresh()
            print("Job in progress...")



def chat():
    print("chat()")
    # MODEL_ENDPOINT = "projects/473040659708/locations/us-central1/endpoints/6990590475795169280" #  LLM 15 epochs
    MODEL_ENDPOINT = "projects/473040659708/locations/us-central1/endpoints/1976395240671543296" # LLM 10 epochs
    #MODEL_ENDPOINT = "projects/473040659708/locations/us-central1/endpoints/8564317070584446976" #spotify 10 epochs
    
    generative_model = GenerativeModel(MODEL_ENDPOINT, system_instruction=[SYSTEM_INSTRUCTION])

    for query in queries:
        print("query: ",query)
        response = generative_model.generate_content(
            [query],  # Input prompt
            generation_config=generation_config,  # Configuration settings
            stream=False,  # Enable streaming for responses
        )
        generated_text = response.text
        print("Fine-tuned LLM Response:", generated_text)
     

def main(args=None):
    print("CLI Arguments:", args)

    if args.train:
        train(args.dataversion)
    
    if args.chat:
        chat()

    if args.foundational_model_chat:
        foundational_model_chat()


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal '--help', it will provide the description
    parser = argparse.ArgumentParser(description="CLI")

    parser.add_argument(
        "--train",
        action="store_true",
        help="Train model",
    )
    parser.add_argument(
        "--chat",
        action="store_true",
        help="Chat with model",
    )

    parser.add_argument(
        "--foundational_model_chat",
        action="store_true",
        help="Chat with foundational model",
    )

    parser.add_argument('--dataversion',
    type=str,
    help="Specify version of data to use for training")

    args = parser.parse_args()

    main(args)
