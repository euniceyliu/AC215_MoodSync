#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

# Set vairables
export BASE_DIR=$(pwd)
export PERSISTENT_DIR=$(pwd)/../persistent-folder/
export SECRETS_DIR=$(pwd)/../secrets/
export GCS_BUCKET_NAME="prompt-playlist-data"
export GCP_PROJECT="ac215-project-438523" # CHANGE TO YOUR PROJECT ID
export GOOGLE_APPLICATION_CREDENTIALS="/secrets/llm-service-account.json"
export IMAGE_NAME="llm-rag-cli"


# Create the network if we don't have it yet
    # network is needed for using multiple services together; ">/dev/null 2>&1" mute errors;
    # inspect network OR|| create network if not found
docker network inspect llm-rag-network >/dev/null 2>&1 || docker network create llm-rag-network

# Build the image based on the Dockerfile
docker build -t $IMAGE_NAME -f Dockerfile .

# # Run Container
docker run --rm --name $IMAGE_NAME -ti \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-v "$PERSISTENT_DIR":/persistent \
-e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
-e GCP_PROJECT=$GCP_PROJECT \
$IMAGE_NAME


# Run All Containers
#docker compose run --rm --service-ports $IMAGE_NAME
#docker run --rm -ti -v "$(pwd)":/app $IMAGE_NAME

### something is not found with this
#docker-compose not found as well
