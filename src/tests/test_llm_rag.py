import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "llm-rag"))

from llm_rag import generate_query_embedding, load, query, chat
from agent_tools import get_chunk_by_filters


class TestLLMRag(unittest.TestCase):

    @patch("llm_rag.TextEmbeddingModel")  # Mock the embedding_model instance
    def test_generate_query_embedding(self, mock_embedding_model):
        # Mock the embedding model's behavior
        mock_embedding_instance = mock_embedding_model.from_pretrained.return_value
        mock_embedding = MagicMock()
        mock_embedding.values = [0.1, 0.2, 0.3]
        mock_embedding_instance.get_embeddings.return_value = [mock_embedding]

        # Define test inputs
        query = "test query"

        # Call the function
        result = generate_query_embedding(query)

        # Assertions
        mock_embedding_instance.get_embeddings.assert_called_once()
        self.assertEqual(result, [0.1, 0.2, 0.3])

    @patch("llm_rag.load_text_embeddings")
    @patch("llm_rag.pd.read_json")
    @patch("llm_rag.chromadb.HttpClient")
    def test_load(self, mock_http_client, mock_read_json, mock_load_text_embeddings):
        mock_client_instance = mock_http_client.return_value

        mock_client_instance.delete_collection.return_value = None

        mock_collection = MagicMock()
        mock_client_instance.create_collection.return_value = mock_collection

        mock_data_df = pd.DataFrame(
            {"text": ["sample text 1", "sample text 2"], "label": [1, 2]}
        )
        mock_read_json.return_value = mock_data_df

        method = "semantic-split-full-lyrics"
        collection_name = f"{method}-song-collection"

        with patch("llm_rag.os.path.join", return_value="mocked_path.jsonl"):
            load(method=method)

        mock_client_instance.delete_collection.assert_called_once_with(
            name=collection_name
        )
        mock_client_instance.create_collection.assert_called_once()
        mock_read_json.assert_called_once_with("mocked_path.jsonl", lines=True)
        mock_load_text_embeddings.assert_called_once_with(mock_data_df, mock_collection)

    @patch("llm_rag.print_results")
    @patch("llm_rag.generate_query_embedding")
    @patch("llm_rag.chromadb.HttpClient")
    def test_query(
        self, mock_http_client, mock_generate_query_embedding, mock_print_results
    ):
        mock_client_instance = mock_http_client.return_value
        mock_collection = MagicMock()
        mock_client_instance.get_collection.return_value = mock_collection
        mock_generate_query_embedding.return_value = [0.1, 0.2, 0.3]
        mock_results = {
            "documents": ["doc1", "doc2", "doc3"],
            "metadata": [{"meta1": "value1"}, {"meta2": "value2"}, {"meta3": "value3"}],
            "distances": [0.1, 0.2, 0.3],
        }
        mock_collection.query.return_value = mock_results

        method = "semantic-split-full-lyrics"
        query(method=method)

        collection_name = f"{method}-song-collection"
        mock_client_instance.get_collection.assert_called_once_with(
            name=collection_name
        )

        self.assertEqual(mock_collection.query.call_count, 3)

    @patch('llm_rag.chromadb.HttpClient')
    @patch('llm_rag.generate_query_embedding')
    @patch('llm_rag.GenerativeModel')
    def test_chat(self, mock_generative_model, mock_generate_query_embedding, mock_chromadb_client):
        mock_generativemodel_instance = mock_generative_model.return_value

        # Mock the query embedding generator
        mock_generate_query_embedding.return_value = [0.1, 0.2, 0.3]

        # Mock the ChromaDB client and collection
        mock_client = MagicMock()
        mock_chromadb_client.return_value = mock_client

        mock_collection = MagicMock()
        mock_client.get_collection.return_value = mock_collection

        # Mock the collection.query() method
        mock_collection.query.return_value = {
            "ids": [["id1", "id2"]],
            "documents": [["doc1", "doc2"]],
        }

        # Mock the generative model's response
        mock_response = MagicMock()
        mock_response.text = "Generated response text"
        mock_generativemodel_instance.generate_content.return_value = mock_response

        # Call the function
        chat_result = chat()

        # Assertions
        mock_chromadb_client.assert_called_once_with(host="llm-rag-chromadb-chat", port=8000)
        mock_client.get_collection.assert_called_once_with(name="semantic-split-full-lyrics-song-collection")
        mock_generate_query_embedding.assert_called_once()
        mock_collection.query.assert_called_once_with(query_embeddings=[[0.1, 0.2, 0.3]], n_results=5)
        mock_generativemodel_instance.generate_content.assert_called_once()
        self.assertEqual(chat_result, "Generated response text")

    def test_get_chunk_by_filters(self):
        # Mock embed_func
        mock_embed_func = MagicMock(return_value=[0.1, 0.2, 0.3])

        # Mock collection with a query method
        mock_collection = MagicMock()
        mock_collection.query.return_value = {
            "ids": [["id1", "id2"]],
            "metadatas": [[{"metadata1": "value1"}, {"metadata2": "value2"}]],
            "documents": [["doc1", "doc2"]]
        }

        # Inputs for the function
        artist = "Beyonce"
        tag = "pop"
        search_content = "Sample content"
        collection = mock_collection
        embed_func = mock_embed_func

        # Call the function
        get_chunk_by_filters(artist, tag, search_content, collection, embed_func)

        # Assertions for embed_func
        mock_embed_func.assert_called_once_with(search_content)

        # Assertions for collection.query
        expected_where_dict = {
            "$or": [{"primary_artist": artist}, {"tags": tag}]
        }
        mock_collection.query.assert_called_once_with(
            query_embeddings=[[0.1, 0.2, 0.3]],
            n_results=10,
            where=expected_where_dict
        )
