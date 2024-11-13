# Preprocessing RAG

## Chunk Documents

Run the `preprocess_rag.py` script with the `--chunk` flag to split your input texts into smaller chunks. Note that for this milestone, we focus on the semantic split because song lyrics and annotations tend to have densely packed meanings in small text segments. The semantic split ensures that each chunk contains coherent and complete ideas, which is crucial for accurate analysis and understanding in later stages of processing. This approach is particularly effective for maintaining the integrity of nuanced content like song lyrics and annotations, where each line can carry significant emotional weight and thematic depth.

```bash
python preprocess_rag.py --chunk --chunk_type char-split
python preprocess_rag.py --chunk --chunk_type recursive-split
python preprocess_rag.py --chunk --chunk_type semantic-split
```
This will read each text file in the Google Cloud Storage and split the lyrics and annotation into chunks using the specified method (character-based or recursive or semantic) the chunks as JSONL files in the outputs directory in Google Cloud.

## Generate Embeddings

```bash
python preprocess_rag.py --embed --chunk_type char-split
python preprocess_rag.py --embed --chunk_type recursive-split
python preprocess_rag.py --embed --chunk_type semantic-split
```
This will generate embeddings for the text chunks. It uses Vertex AI's text embedding model to generate embeddings for each chunk and saves the chunks with their embeddings as new JSONL files. We use Vertex AI text-embedding-004 model to generate the embeddings

## Load Embeddings into Vector Database

```bash
python preprocess_rag.py --load --chunk_type char-split
python preprocess_rag.py --load --chunk_type recursive-split
python preprocess_rag.py --load --chunk_type semantic-split
```
This will connect to the ChromaDB instance and then load the dataframe from the created embeddings and metadata.

## Query the Vector Database

```bash
python preprocess_rag.py --query --chunk_type char-split
python preprocess_rag.py --query --chunk_type recursive-split
python preprocess_rag.py --query --chunk_type semantic-split
```
We further test whether our created collection is sucessful by querying it. This will generate an embedding for a sample query and perform similarity searches in the vector database. Besides, we can also query specific text in the collection.
