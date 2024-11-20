

# AC215 - Milestone4 - MoodSync: AI-Powered Playlists for Emotional Resonance

## Project Information
**Team Members**
Eunice Liu (youchiliu@fas.harvard.edu)
Megan Luu (meganluu@g.harvard.edu)
Xinyu Chen (xinyuchen@hms.harvard.edu)

**Group Name**
MoodSync Group

**Description**
In this project, we aim to develop an AI-powered music recommendation tool. The tool will feature a chatbot designed to analyze text input from users about their current mood and music preferences, such as favorite artists and genres. Users can input descriptions of their feelings and musical tastes, and the chatbot will generate a personalized playlist tailored to their emotional state and preferences. It will be powered by a RAG model and fine-tuned models, making it a specialist in personalized music playlist curation.


## Milestone 4 ##

**Overview of this Milestone**

For this milestone, we implemented CI/CD workflows in GitHub Actions to test our code, developed a functional front-end for our website with React, and created APIs for our source code to have robust integration between the frontend and backend of the user-facing application.

**Milestone 4 Deliverables**
1. Application Design Document: Our application design document detailing the solution and technical architecture can be found in this [Google Doc](https://docs.google.com/document/d/16WsrRdNQLMYpk2EwI2zTQYp2RJXBQh1r6QnW85Rp1cc/edit?usp=sharing).
2. APIs & Frontend Implementation: The functional code for the backend APIs and frontend can be found in the [`src/api-service`](src/api-service) and [`src/frontend`](src/frontend) folders, respectively. Each of the folders also have README.md files that describe the application components, setup instructions, and usage guidelines.
3. Continuous Integration Setup, Automated Testing Implementation, Test Documentation: We have set up a Github Actions workflow to run our unit/integration tests and flake8 on every push, and it provides a coverage report as an artifact after the workflow run -- this can be found under the Actions tab. The GitHub Actions configuration file can be found under [`.github/workflows/test.yml`](.github/workflows/test.yml). The tests check the core functionality of some of the main components of our app pipeline. Detailed documentation of the tests can be found in [`src/tests`](src/tests).

**Instructions for running the app**

Ensure you have the correct permissions and GCP credentials in the secrets folder. 
1. Open a terminal window and navigate to `src/vector-db`. Run `sh docker-shell.sh` to start the container. Run `python llm_rag.py --load` to load the vector database collection. Keep this container running.
2. Navigate to `src/api-service`. Run `sh docker-shell.sh` to start the container and run `uvicorn_server`. Keep this container running.
3. Open a new terminal window and navigate to `src/frontend`. Run `sh docker-shell.sh` to start the container and run `npm dev run` to start the application. 

**Demo**
[![Website](https://i.sstatic.net/Vp2cE.png)]((https://drive.google.com/file/d/1wUkXAh0tubQsR-h66x-bWkb86CLHgmkN/preview))

## Project's Key Components Overview

1.**`src/dataset-creation/dataset-creation/cli.py`**
   This script performs the data generation and uploads the collected data into the google bucket.

2.**`src/finetune-llm/finetune-llm/cli.py`**
   This script performs the communication with the foundation models, adjusting prompting, and fine-tuning of LLM models.

3.**`src/datapipeline/preprocess_rag.py`**
   This script prepares the necessary data for setting up our vector database. It performs chunking, embedding, and loads the data into a vector database (ChromaDB). It also include a querying function to test if our database is created successfully or not.

4.**`src/llm-rag/llm_rag.py`**
   This script currently loads the preprocessed data into chromadb, and then generate response using the user's query, most relevant entry from a RAG search in the chromadb container, and a pre-set prompt from a foundation LLM model.

5.**`src/api-service`**
   This folder compiles the relevant source code and files used to create FastAPI functions to host the backend of the website and link it to the frontend.

6.**`src/frontend`**
   This folder contains the files necessary to build the frontend using React.

7.**`src/tests`**
   This folder contains unit tests and integration tests that run with Github Actions workflow to ensure efficient testing of our code with every push.

## Directory

```
├── Readme.md
├── LICENSE
├── results
│   └── experiments
│   └── images
├── notebooks
│   └── eda.ipynb
│   └── finetunedata_preprocessing.ipynb
├── reports
│   └── MoodSync_Proposal.pdf
└── src
    ├── dataset-creation
    │   ├── env.dev
    │   ├── dataset-creation
    │   │   ├── cli.py
    │   │   ├── docker-entrypoint.sh
    │   │   ├── docker-shell.sh
    │   │   ├── Dockerfile
    │   │   ├── Pipfile
    │   │   ├── Pipfile.lock
    │   │   └── spotify_playlist_data.csv
    ├── data-versioning
    │   ├── docker-entrypoint.sh
    │   ├── docker-shell.sh
    │   ├── Dockerfile
    │   ├── Pipfile
    │   ├── Pipfile.lock
    │   ├── promptdata.csv.dvc
    │   └── prompts.txt.dvc
    ├── finetune-llm
    │   ├── env.dev
    │   ├── finetune-llm
    │   │   ├── cli.py
    │   │   ├── docker-entrypoint.sh
    │   │   ├── docker-shell.sh
    │   │   ├── Dockerfile
    │   │   ├── Pipfile
    │   │   └── Pipfile.lock
    ├── datapipeline
    │   ├── docker-entrypoint.sh
    │   ├── docker-shell.sh
    │   ├── Dockerfile
    │   ├── Pipfile
    │   ├── Pipfile.lock
    │   ├── semantic_splitter.py
    │   ├── preprocess_rag.py
    │   └── docker-compose.yml
    ├── llm-rag
    │   ├── docker-entrypoint.sh
    │   ├── docker-shell.sh
    │   ├── Dockerfile
    │   ├── Pipfile
    │   ├── Pipfile.lock
    │   ├── semantic_splitter.py
    │   ├── llm_rag.py
    │   └── docker-compose.yml
    └── secrets

```
----
