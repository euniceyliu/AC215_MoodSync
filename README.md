

# AC215 - Milestone2 - MoodSync: AI-Powered Playlists for Emotional Resonance

## Project Information
**Team Members**
Eunice Liu (youchiliu@fas.harvard.edu)
Megan Luu (meganluu@g.harvard.edu)
Xinyu Chen (xinyuchen@hms.harvard.edu)

**Group Name**
MoodSync Group

**Description**
In this project, we aim to develop an AI-powered music recommendation tool. The tool will feature a chatbot designed to analyze text input from users about their current mood and music preferences, such as favorite artists and genres. Users can input descriptions of their feelings and musical tastes, and the chatbot will generate a personalized playlist tailored to their emotional state and preferences. It will be powered by a RAG model and fine-tuned models, making it a specialist in personalized music playlist curation.

**Overview of this Milestone**

## Data
1. The Genius Expertise Dataset consists of public user and song information from [genius.com](https://genius.com/), focusing on song lyrics, annotations, and artists informations. Collected through web crawls from September 2019 to January 2020, this dataset includes annotations of the lyrics from users and artists that can be valuable for building the RAG model by leveraging the insights and interpretations embedded in the annotations. The dataset was cited as follows: Lim, Derek, and Austin R. Benson. "Expertise and Dynamics within Crowdsourced Musical Knowledge Curation: A Case Study of the Genius Platform." Proceedings of the International Conference on Web and Social Media (ICWSM), 2021. The data file can be accessed [here](https://github.com/cptq/genius-expertise/tree/master/data). This dataset can significantly enhance the understanding of lyrical interpretations and user contributions, making it a useful resource for research and model development in music annotation and analysis. We stored the dataset in our private Google Cloud Platform bucket.
2. The [Spotify Million Playlist](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge) dataset consists of user-generated playlists with titles & descriptions. The titles and descriptions often refer to music categories (genre, artist, year, etc.), mood, themes, or occasions. Thus, we experimented with this dataset in fine-tuning to allow the LLM to better learn associations between playlist content and music categories/moods. To understand the preprocessing steps before we used the data for fine-tuning, please refer to the dataset-creation documentation.
3. LLM-Generated Prompt-Response pairs were generated using carefully curated prompt instructions to target areas of performance improvement in the playlist recommendations. Specifically, this dataset contains example prompts that utilize modern day slang, as well as vague prompts that do not explicitly ask for playlists. This dataset was also used in fine-tuning experimentation to allow the LLM to better learn a preferred output format and persona. To understand the complete data generation and preprocessing steps for this dataset, please refer to the dataset-creation documentation.

**Data Pipeline Containers**
1. One container processes the 100GB dataset by resizing the images and storing them back to Google Cloud Storage (GCS).

	**Input:** Source and destination GCS locations, resizing parameters, and required secrets (provided via Docker).

	**Output:** Resized images stored in the specified GCS location.

2. Another container prepares data for the RAG model, including tasks such as chunking, embedding, and populating the vector database.

## Data Pipeline Overview

1. **`src/datapipeline/preprocess_rag.py`**
   This script prepares the necessary data for setting up our vector database. It performs chunking, embedding, and loads the data into a vector database (ChromaDB). It also include a querying function to test if our database is created successfully or not.

2. **`src/datapipeline/Pipfile`**
   We used the following packages to help with preprocessing:
   - `special cheese package`

3. **`src/preprocessing/Dockerfile(s)`**
   Our Dockerfiles follow standard conventions, with the exception of some specific modifications described in the Dockerfile/described below.


## Running Dockerfile
Instructions for running the Dockerfile can be added here.
To run Dockerfile - `Instructions here`

**Models container**
- This container has scripts for model training, rag pipeline and inference
- Instructions for running the model container - `Instructions here`

**Notebooks/Reports**
This folder contains code that is not part of container - for e.g: Application mockup, EDA, any 🔍 🕵️‍♀️ 🕵️‍♂️ crucial insights, reports or visualizations.

#### Project Milestone 2 Organization

```
├── Readme.md
├── data # DO NOT UPLOAD DATA TO GITHUB, only .gitkeep to keep the directory or a really small sample
├── notebooks
│   └── eda.ipynb
├── references
├── reports
│   └── Statement of Work_Sample.pdf
└── src
    ├── datapipeline
    │   ├── Dockerfile
    │   ├── Pipfile
    │   ├── Pipfile.lock
    │   ├── dataloader.py
    │   ├── docker-shell.sh
    │   ├── preprocess_cv.py
    │   ├── preprocess_rag.py
    ├── docker-compose.yml
    └── models
        ├── Dockerfile
        ├── docker-shell.sh
        ├── infer_model.py
        ├── model_rag.py
        └── train_model.py
```
----
You may adjust this template as appropriate for your project.
