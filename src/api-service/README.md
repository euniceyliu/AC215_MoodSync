# API Backend Implementation

## Component Overview
This folder contains the code to implement the backend core functionalities of our application.
`api-service/routers` defines the routers for the APIs that call the functions defined in utils.
`api-service/utils` contains the util functions that define the functionalities required for our website, namely, generating a response from the LLM and querying the vector database to supplement the LLM's response.

## Setup Instructions
1. Open a terminal window and navigate to `src/vector-db`. Run `sh docker-shell.sh` to start the container. Run `python llm_rag.py --load` to load the vector database collection. Keep this container running.
2. Navigate to `src/api-service`. Run `sh docker-shell.sh` to start the container and run `uvicorn_server`.

We can check [http://localhost:9000/docs](http://localhost:9000/docs) to confirm that all our routers are connected and working properly.

![Screenshot 2024-11-20 at 12 05 14 AM](https://github.com/user-attachments/assets/5c5b5f69-8d98-43f4-83e8-954abd5daee4)
