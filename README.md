## Milestone 2 Template

```
The files are empty placeholders only. You may adjust this template as appropriate for your project.
Never commit large data files,trained models, personal API Keys/secrets to GitHub
```

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

# AC215 - Milestone2 - MoodSync: AI-Powered Playlists for Emotional Resonance

**Team Members**
Eunice Liu (youchiliu@fas.harvard.edu)
Megan Luu (meganluu@g.harvard.edu)
Xinyu Chen (xinyuchen@hms.harvard.edu)

**Group Name**
MoodSync Group

**Project**
In this project, we aim to develop an AI-powered music recommendation tool. The tool will feature a chatbot designed to analyze text input from users about their current mood and music preferences, such as favorite artists and genres. Users can input descriptions of their feelings and musical tastes, and the chatbot will generate a personalized playlist tailored to their emotional state and preferences. It will be powered by a RAG model and fine-tuned models, making it a specialist in personalized music playlist curation.

### Milestone2 ###

In this milestone, we have the components for data management, including versioning, as well as the computer vision and language models.

**Data**
We gathered a dataset of 100,000 cheese images representing approximately 1,500 different varieties. The dataset, approximately 100GB in size, was collected from the following sources: (1), (2), (3). We have stored it in a private Google Cloud Bucket.
Additionally, we compiled 250 bibliographical sources on cheese, including books and reports, from sources such as (4) and (5).

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

----
You may adjust this template as appropriate for your project.
