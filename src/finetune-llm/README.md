# Finetuning LLM

This folder contains the files required to implement a containerized pipeline to finetune LLMs.

## Run the container
To run the container, navigate to the finetune-llm folder in the terminal and run:

`sh docker-shell.sh`


## Foundation Model Chat
To chat with the foundational `gemini-1.5-flash-002` LLM model, run:

`python cli.py --foundational_model_chat`

This will send the predefined queries in `cli.py` to the model and print out the responses.

## Train the model
To fine-tune the model, run:

`python cli.py --train --dataversion v{insert-number}`

This will fine-tune the model on the data version found in the GCS bucket `gs://prompt-playlist-data/{dataversion}/`

## Chat with the fine-tuned model
After completing fine-tuning, run:

`python cli.py --chat`

This will send the predefined queries in `cli.py` to the fine-tuned model and print out the responses.

## Fine-Tuning Experimentation
Please refer to the experimentation folder for details on fine-tuning experiments for Milestone 2.