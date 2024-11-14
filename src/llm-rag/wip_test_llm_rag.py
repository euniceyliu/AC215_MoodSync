import unittest
from unittest.mock import patch, MagicMock, call
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(
    0, 
    str(
        Path(__file__)
        .resolve()
        .parent
        .parent / "llm-rag"
    )
)

from llm_rag import generate_query_embedding, load, query, chat



class TestLLMRag(unittest.TestCase):

    @patch("llm_rag.embedding_model.get_embeddings")  
    @patch("llm_rag.TextEmbeddingInput")  
    def test_generate_query_embedding(self, mock_text_embedding_input, mock_get_embeddings):
        """Tests the functionality of the generate query embedding function"""
        mock_query_embedding_input = MagicMock()
        mock_text_embedding_input.return_value = mock_query_embedding_input
        
        mock_embedding = MagicMock()
        mock_embedding.values = [0.1, 0.2, 0.3] 
        mock_get_embeddings.return_value = [mock_embedding]

        query = "test query"
        result = generate_query_embedding(query)

        mock_text_embedding_input.assert_called_once_with(task_type="RETRIEVAL_DOCUMENT", text=query)
        mock_get_embeddings.assert_called_once()
        self.assertEqual(result, [0.1, 0.2, 0.3])


    @patch("llm_rag.load_text_embeddings")  
    @patch("llm_rag.pd.read_json")  
    @patch("llm_rag.chromadb.HttpClient")  
    def test_load(self, mock_http_client, mock_read_json, mock_load_text_embeddings):
        mock_client_instance = mock_http_client.return_value

        mock_client_instance.delete_collection.return_value = None

        mock_collection = MagicMock()
        mock_client_instance.create_collection.return_value = mock_collection

        mock_data_df = pd.DataFrame({
            "text": ["sample text 1", "sample text 2"],
            "label": [1, 2]
        })
        mock_read_json.return_value = mock_data_df

        method = "semantic-split-full-lyrics"
        collection_name = f"{method}-song-collection"

        with patch("llm_rag.os.path.join", return_value="mocked_path.jsonl"):
            load(method=method)

        mock_client_instance.delete_collection.assert_called_once_with(name=collection_name)
        mock_client_instance.create_collection.assert_called_once()
        mock_read_json.assert_called_once_with("mocked_path.jsonl", lines=True)
        mock_load_text_embeddings.assert_called_once_with(mock_data_df, mock_collection)

    @patch("llm_rag.print_results")  
    @patch("llm_rag.generate_query_embedding") 
    @patch("llm_rag.chromadb.HttpClient") 
    def test_query(self, mock_http_client, mock_generate_query_embedding, mock_print_results):
        mock_client_instance = mock_http_client.return_value
        mock_collection = MagicMock()
        mock_client_instance.get_collection.return_value = mock_collection
        mock_generate_query_embedding.return_value = [0.1, 0.2, 0.3]
        mock_results = {
            "documents": ["doc1", "doc2", "doc3"],
            "metadata": [{"meta1": "value1"}, {"meta2": "value2"}, {"meta3": "value3"}],
            "distances": [0.1, 0.2, 0.3]
        }
        mock_collection.query.return_value = mock_results

        method = "semantic-split-full-lyrics"
        query(method=method)

        collection_name = f"{method}-song-collection"
        mock_client_instance.get_collection.assert_called_once_with(name=collection_name)

        self.assertEqual(mock_collection.query.call_count, 3)

