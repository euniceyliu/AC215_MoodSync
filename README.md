

# AC215 - Milestone 5 - MoodSync: AI-Powered Playlists for Emotional Resonance

## Project Information
**Team Members**
Eunice Liu (youchiliu@fas.harvard.edu)
Megan Luu (meganluu@g.harvard.edu)
Xinyu Chen (xinyuchen@hms.harvard.edu)

**Group Name**
MoodSync Group

**Description**
In this project, we aim to develop an AI-powered music recommendation tool. The tool will feature a chatbot designed to analyze text input from users about their current mood and music preferences, such as favorite artists and genres. Users can input descriptions of their feelings and musical tastes, and the chatbot will generate a personalized playlist tailored to their emotional state and preferences. It will be powered by a RAG model and fine-tuned models, making it a specialist in personalized music playlist curation.


## Milestone 5 ##

**Overview of this Milestone**

For this final milestone, we used Ansible playbooks to automate the provisioning and deployment of our infrastructure and application to a Kubernetes cluster. We also have a working CI/CD pipeline which runs unit tests (`.github/workflows/test.yml`) and automates the deployment of updates upon pushes to the main branch (`.github/workflows/deployment-cicd.yml`). We demonstrate the full machine learning workflow, starting from data preprocessing in the `src/dataset-creation` and `src/datapipeline` folders, to the model training and evaluation in `src/finetune-llm` folder.

**Instructions for deploying the app**

- Prerequisites and setup instructions:
  
Ensure that you have the required GCP credentials (i.e. deployment.json, gcp-service.json) in the secrets folder. These credentials should allow permission to Compute Admin, Compute OS Login, Container Registry Service Agent, Kubernetes  Engine Admin, Service Account User, Storage Admin, Vertex AI Administrator, and Artifact Registry Administrator roles.

- Deployment instructions:

  1. Navigate to the `src/deployment` folder.

  2. Run `sh docker-shell.sh` to start the container for deployment.

  3. If the app Docker images have never been pushed to the GCR before, run:

  ```ansible-playbook deploy-docker-images.yml -i inventory.yml```

  4. To start the Kubernetes cluster and deploy the application, run:

  ```ansible-playbook deploy-k8s-cluster.yml -i inventory.yml --extra-vars cluster_state=present```

  (note that this will take some time if the cluster is not already running)

  5. The terminal will output an `nginx_ingress_ip`, and the application is now accessible at `http://<YOUR INGRESS IP>.sslip.io`.

- Usage details and examples:
  
The application can be used to request playlist recommendations based on one's music preferences and current mood. Users can input their current status as well artists, genres, and/or song topics that they prefer in order to get their custom playlist.

Example #1: Asking for playlist by genre

https://github.com/user-attachments/assets/65a95946-437c-4609-8dea-8d9807c4a421


Example #2: Asking for playlist by song topic

https://github.com/user-attachments/assets/09d730c8-dfe6-485f-8480-217e3102cb28

  
- Known issues and limitations:
  
Currently, a limitation of our application is that the music database used for RAG does not automatically incorporate new music as it comes out. Thus, the playlist recommendations does not update with new music over time. To address this limitation, future work would involve developing a pipeline to scrape data from Genius.com as new lyrics and annotations for songs come out, and incorporate them into our vector database. Another limitation is that the application currently does not support conversation memory - thus, users are unable to continue their previous conversation and amend playlists based on what the chatbot has previously learned about them. 


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

8.**`src/deployment`**
   This folder contains Ansible playbook and relevant files to deploy the application to Kubernetes cluster.

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
