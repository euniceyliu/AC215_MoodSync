# CI Tests

The unit tests and integration tests for the app components are contained in this folder.
Because most of our components extensively use GCP services and the Vertex AI API and call for generated responses by LLMs, we had to use mock and patch methods from 
the unittest package in order to simulate these API requests and test the functionality of the modules.

## Automated Testing Implementation using Github Actions
These tests are integrated into a GitHub Actions workflow to run automatically after a push to the milestone4 branch. The GitHub Action workflow automatically runs the test files in this folder and runs flake8 to ensure code quality and proper formatting. After completing the tests, the workflow also automatically uploads the coverage reports as artifacts after the run, which can be downloaded on the workflow summary page.  Currently, all our test cases pass with over 50% coverage.

<img width="698" alt="Screenshot 2024-11-17 at 10 14 55 PM" src="https://github.com/user-attachments/assets/0a2cee93-6d06-43b8-a22d-e0e66f4d478a">

## Instructions to run locally
To run these tests locally, 
1. From the root of the repo, run
 ``docker build -t test-image -f src/Dockerfile .``.
2. Then run the container using ``docker run -it test-image sh``
3. Run the tests using ``pipenv run pytest -v``.

## Test Documentation
All of our test functions utilize pytest and unittest methods:

**test_dataset_creation.py**

-``test_generate_data``: This test evaluates the functionality of the ``generate_data`` function, ensuring it correctly integrates with a generative model to produce output and write the generated content to a file. It mocks the GenerativeModel class and simulates a mock response for content generation. The test also verifies that the file writing operation is invoked as expected, ensuring seamless interaction between the data pipeline and file handling components.

-``test_generate_data_llm``:This test focuses on the ``generate_data_llm`` function, ensuring it generates content iteratively using a mock generative model for a pre-determined number of iterations. It verifies that the content generation method is called the expected number of times and that the generated content is written to the file during each iteration. This test confirms the function's behavior in handling multiple calls to the LLM and managing file outputs.

-``test_prepare``: This test verifies the prepare function, which processes prompt-response data into a structured DataFrame and creates train and test datasets. It mocks the file reading process, simulates parsing of JSON data, and ensures that the data transformation logic works as intended. The test checks if the processed DataFrame is saved as a CSV file and whether the train and test splits are written to JSONL files. It validates end-to-end preparation of data for fine-tuning a generative model.

-``test_upload``: This test validates the upload function, which uploads files to a storage bucket. It simulates retrieving files with specific extensions (.jsonl, .csv, .txt) using glob and mocks interactions with a cloud storage client to ensure files are uploaded correctly. The test checks that file paths are correctly joined and uploaded to the appropriate versioned bucket, ensuring robust integration with the cloud storage system.

**test_llm_rag.py**

-``test_generate_query_embedding``: This test ensures the functionality of the ``generate_query_embedding`` function, which uses a text embedding model to compute embeddings for a given query. By mocking the TextEmbeddingModel and its behavior, the test verifies that the embedding model is called once and that the correct embedding values are returned. It confirms the function's ability to handle query inputs and interact correctly with the embedding model.

-``test_load``: This test validates the ``load`` function, which integrates text data with a vector database for semantic querying. The test mocks the deletion and creation of collections in a vector database client and ensures that the data is read from a JSONL file correctly. It also verifies that text embeddings are loaded into the newly created collection. This test confirms that the function handles the preprocessing and loading pipeline for semantic text data efficiently.

-``test_query``: This test evaluates the ``query`` function, which retrieves relevant documents and metadata from a vector database based on a query embedding. By mocking the embedding generation and database interactions, the test ensures that the query is processed correctly, and results are retrieved from the collection. It also verifies that the function calls the appropriate methods in the database client and processes query results correctly, validating its end-to-end retrieval pipeline.

-``test_chat``: This test validates the core functionality of the ``chat`` function, which integrates multiple components such as embedding generation, querying a ChromaDB collection, and generating a response using a generative model. The test ensures:
The generate_query_embedding function produces embeddings based on the query text.
The ChromaDB client retrieves the correct collection and queries it using the generated embeddings.
The generative model processes the retrieved results and produces the final response. This test checks the end-to-end flow of the chat function, ensuring all dependencies are invoked correctly and the final output matches expectations.

-``test_get_chunks_by_filters``: This test focuses on verifying the behavior of the get_chunk_by_filters function from the agent tools, which filters content based on specified criteria (artist and tag). It ensures:
The embedding generation function is called with the correct input (search_content).
The query to the ChromaDB collection uses the correct filtering logic (artist, tag, or both) and embeddings.
The number of results retrieved matches the specified limit (10). This test validates the filtering and querying logic of the function, ensuring that the filters and embeddings are applied correctly to retrieve the desired content.
