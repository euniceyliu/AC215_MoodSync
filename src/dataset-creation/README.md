# Dataset Creation Pipeline

This folder contains the files required to implement a containerized dataset creation pipeline to finetune LLMs.

## Run the container
To run the container, open a terminal in the data-creation folder and run:

`sh docker-shell.sh`

## Generate data based on Spotify playlist dataset
Using the preprocessed Spotify playlist data with columns 'songs', 'title', 'description', run:

`python cli.py --generate_data --file spotify_playlist_data.csv`

This will call an LLM to process each row in the dataset and generate corresponding natural language user prompt and playlist recommendation response pairs.
It uses the following system instruction to instruct the LLM on how to generate the data:
```
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
```

This code was also used to generate the input prompt, assuming `row` is a row in the Spotify playlist dataset:

```python
songs = row['songs']
title = row['title']
description = row['description']
query = f"Playlist Title: {title}, Description: {description}, Songs: {songs}"
```

These are sample prompt and response pairs from running this process:
| Prompt | Response |
|----------|----------|
|   I need some songs that are total emotional bangers.  Heartbreak anthems, songs about overcoming struggles, and some chill vibes for when I need to just breathe. Think raw emotion, vulnerability, and maybe a little bit of hope thrown in.  |   Oh, I totally get it.  Sometimes you just need music that speaks to your soul, right?  It sounds like you're looking for a mix of emotional depth and some chill vibes to balance things out. This playlist is gonna be a real emotional rollercoaster, but in the best way possible! Get ready to feel ALL the feels. <br> Here's a playlist that's got your back: <br> **Not In That Way - Sam Smith:** This song perfectly captures that longing and vulnerability when you're drawn to someone but know it can't be.  It's a classic for a reason!...   |
|  Yo, I need some fire tunes from UK bands, like, some fresh bangers that just dropped.  Think rock, but with a chill vibe, perfect for a cuppa.  Hit me with the sauce.  |   Hey there! I totally get you -- sometimes you just need that perfect blend of energetic rock and relaxed vibes, especially with a warm cuppa in hand.  This playlist is gonna be a total slap! Let's dive into some fresh tunes from UK bands: <br> **Vampires - Frank Carter & The Rattlesnakes:** This track is pure energy, perfect for headbanging while still enjoying the comfort of your beverage. It's got a raw and powerful sound that's impossible to ignore...   |

## Prepare the Spotify-based dataset for finetuning
Run:
`python cli.py --prepare`

This will prepare the previously created data in a format that is compatible for fine-tuning gemini models in Vertex AI. It performs a train test split and creates the train.jsonl and test.jsonl files that will be used for fine-tuning the LLM model.

## Alternatively, generate data without a playlist dataset by using an LLM
Part of our fine-tuning experimentation involved using different datasets to finetune the LLM. Thus, rather than using the user-generated playlists from the Spotify playlist dataset, we also used an LLM to generate prompt-response pairs that mimic a user's interaction with an AI playlist generator.
Run:

`python cli.py --generate_data_llm`

We used the following system instructions to instruct the LLM on how to generate the data:
```
"""Generate 15 prompt & response pairs resembling a user's interaction with an AI personalized playlist recommendation system.
Each prompt must be 1-2 sentences and contain information about the user's emotion and/or their music preferences such as artists or genre. Ensure all the prompts are unique, each using a specific tone. Adhere to the following guidelines:
1. Some prompts must use a variety of modern trendy slang words such as 'sauce', 'slap', 'fire', 'wavy', 'slay'. You may use these words and other slang words.
2. Some prompts must not explicitly ask for a playlist, but rather just state the user's current context or mood, i.e. 'I have an exam tomorrow.'
3. Some prompts must be an abstract feeling with imagery, i.e. 'I'm walking through the busy streets of a big city.' Do not copy this example
4. Some prompts must consist of only a list of concepts that allude to a feeling, i.e. 'cocoa, pumpkins, knitting'. Do not copy this example.


Next, assume you are the expert at recommending personalized playlists. Generate the response that adheres to the following guidelines:
1. Acknowledge that you understand the user's mood and paraphrase what they're looking for. Use an empathetic and enthusiastic tone.
2. Cater to the tone of the user. For example, if they use slang, you can speak conversationally and casual. If they are sad, use a gentle and comforting tone.
3. Select songs that are most relevant based on the user's mood and music preferences. If there is not enough information provided by the user, provide a preliminary playlist, but encourage them to share more information.
4. Present a maximum of 15 songs in the playlist, and provide a brief explanation as to why each song is included in the playlist. The explanations should be brief but informative and unique.
5. Conclude the response with words of encouragement, with a brief statement about how this music is a great complement to their current situation.

Output Format:
Provide the Prompt and Response pairs in the following format, but do not copy the example:
[{"prompt": "I'm feeling lost.","response": "I'm really sorry you're feeling lost right now. That can be such a tough and confusing place to be. Let me create a playlist that gives you some space to reflect, with calming, grounding tracks and a few uplifting ones that gently remind you you're not alone.\n**Holocene – Bon Iver** A hauntingly beautiful song that captures feelings of introspection and searching for meaning.\n**Lost in the Light – Bahamas** A mellow, soothing track that feels like a gentle reminder that it's okay to not have everything figured out.\n**River – Leon Bridges** A soulful and calming song about seeking peace and redemption.  I hope these tracks bring you a sense of comfort and help you navigate through the emotions you're experiencing."}]
"""
We also provide the LLM input prompt:
`Generate 15 prompt & response pairs. Ensure each pair is independent and unique.`
and iterated over this prompt 5 times.

```
These are sample prompt and response pairs from running this process:
| Prompt | Response |
|----------|----------|
|   Coffee, rain, cozy blankets.  |   Ahh, the perfect trifecta for a cozy day! Let's soundtrack this with a playlist that will snuggle your soul.  <br>**1. 'Harvest Moon' - Neil Young:** Warm and mellow folk perfect for the mood. <br> **2. 'Shelter Song' - Temples:** Dreamy tunes...  |
|   I need some fire beats to hype me up for a workout! Something super wavy and fresh |   Let's get those muscles pumpin' with a wavy workout playlist! 🔥  <br>**Blinding Lights - The Weeknd:**  Unmatched energy, a definite cardio booster.<br>**Don't Start Now - Dua Lipa:** An absolute banger that keeps you moving. |

## Prepare the LLM-generated dataset for finetuning
Run:

`python cli.py --prepare_llm`

## Upload the generated dataset to GCS Bucket
Whether you used the Spotify-based dataset or the LLM method to generate the fine-tuning dataset, run:

`python cli.py --upload --version v{insert-number}`

This will upload all the relevant datafiles to the project's Google Cloud Storage bucket, under the folder of the provided version number. For example, if we specify
version to be v1, the datafiles can be found in the GCS bucket folder `prompt-playlist-data/v1/`.


This concludes the containerized data-generation pipeline. The next step is to fine-tune the LLM on these datasets; the pipeline for that step can be found in finetune-llm folder in the repo.
