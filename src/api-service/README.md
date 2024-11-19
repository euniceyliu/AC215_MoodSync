# instructions
This folder contains the files required to run the backend of the app, and instructions to connect it to the frontend

## Data preparation
1. Run the container:
     To run the container, navigate to the datapipeline folder in the terminal and run: `sh docker-shell.sh`
2. Inside the container, run `python preprocess_rag.py --load --chunk_type semantic-split` to collected the processed data from the google bucket.
3. Exit the container.
4. If another container is using port 8000, check the process with `sudo lsof -i :8000` and kill the process with `kill -9 <pid>`

## API
5. Run the container:
     To run the container, navigate to the api-service folder in the terminal and run: `sh docker-shell.sh`
6. Inside the container, run `uvicorn_server` and Verify service is running at http://localhost:9000
7. Keep the container running, and proeceed to the next steps. (the API container needs to be running for the frontend container to connect to it)

## Connect frontend
8. Run the container:
     To run the container, navigate to the front-end folder in the terminal and run: `sh docker-shell.sh`
9. Inside the container, `npm install` and then `npm run dev` to start the development server
10. View and use the app at: http://localhost:3000
