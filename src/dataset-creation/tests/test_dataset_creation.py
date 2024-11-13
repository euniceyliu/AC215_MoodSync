import unittest
from unittest.mock import patch, MagicMock, call
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src/dataset-creation')))
from cli import generate_data, generate_data_llm, prepare, upload

class TestGenerateData(unittest.TestCase):
    @patch("cli2.GenerativeModel")  
    @patch("builtins.open", create=True) 
    def test_generate_data(self, mock_open, mock_generative_model):
        """Tests functionality of generate_data function"""
        test_data = {
            "songs": ["Song1, Song2"],
            "title": ["Chill Vibes"],
            "description": ["A relaxing playlist for unwinding."],
        }
        df = pd.DataFrame(test_data)

        with patch("pandas.read_csv", return_value=df):

            mock_response = MagicMock()
            mock_response.text = "Generated content response"
            mock_generative_model_instance = mock_generative_model.return_value
            mock_generative_model_instance.generate_content.return_value = mock_response
            mock_generative_model_instance.generation_config = {
                                    "max_output_tokens": 5000, 
                                    "temperature": 1.85,  
                                    "top_p": 0.97,  
                                }

            # Call the function
            generate_data("dummy_file_path.csv")

            query = (
                "Playlist Title: Chill Vibes, Description: A relaxing playlist for unwinding., "
                "Songs: Song1, Song2"
            )
   
            # Assert generate_content was called 
            mock_generative_model_instance.generate_content.assert_called_once()

            # Check if file writing was called with expected content
            mock_open.assert_called_once_with("prompt_playlist_data.txt", "a")


    @patch("cli2.GenerativeModel")  # Mock the GenerativeModel class in cli2
    @patch("builtins.open", create=True)  # Mock the open function to avoid file I/O
    def test_generate_data_llm(self, mock_open, mock_generative_model):
        "Tests functionality of generate_data_llm function"
        mock_response = MagicMock()
        mock_response.text = "Generated content response"
        mock_generative_model_instance = mock_generative_model.return_value
        mock_generative_model_instance.generate_content.return_value = mock_response
        mock_generative_model_instance.generation_config = {
            "max_output_tokens": 5000,
            "temperature": 1.85,
            "top_p": 0.97
        }
        
        # Call the function
        generate_data_llm()

        # Verify that generate_content was called the expected number of times
        num_iterations = 5  
        self.assertEqual(
            mock_generative_model_instance.generate_content.call_count, num_iterations
        )
        # Check if file writing was called 
        self.assertEqual(
            mock_open.call_count, num_iterations
        )


    @patch("builtins.open", create=True)  # Mock open function
    @patch("cli2.train_test_split")  # Mock train_test_split
    @patch("cli2.pd.DataFrame.to_csv")  # Mock DataFrame.to_csv to avoid file I/O
    @patch("cli2.pd.DataFrame.to_json")  # Mock DataFrame.to_json to avoid file I/O
    def test_prepare(self, mock_to_json, mock_to_csv, mock_train_test_split, mock_open):
        """Tests functionality of prepare function"""
        mock_text = """```json
        [
            {"prompt": "Sample prompt 1", "response": "Sample response 1"},
            {"prompt": "Sample prompt 2", "response": "Sample response 2"}
        ]
        ```"""


        mock_open.return_value.read.return_value = mock_text

        mock_json_data = [
            {"prompt": "Sample prompt 1", "response": "Sample response 1"},
            {"prompt": "Sample prompt 2", "response": "Sample response 2"}
        ]
        
        # Mock json.loads to return structured data for DataFrame creation
        with patch("cli2.json.loads", return_value=mock_json_data):

            final_df = pd.DataFrame(mock_json_data)
            final_df["contents"] = final_df.apply(
                lambda row: [
                    {"role": "user", "parts": [{"text": row["prompt"]}]},
                    {"role": "model", "parts": [{"text": row["response"]}]}
                ],
                axis=1
            )

            df_train = final_df.head(1)  
            df_test = final_df.tail(1)   
            mock_train_test_split.return_value = (df_train, df_test)

            prepare()

            # Verify `open` was called to read the initial file
            mock_open.assert_any_call("prompt_playlist_data.txt", "r")
            # Verify that to_csv was called to save `final_df`
            mock_to_csv.assert_called_once_with("finetune_df.csv", index=False)

            # Verify JSON writing for train and test sets
            mock_open.assert_any_call("train.jsonl", "w")
            mock_open.assert_any_call("test.jsonl", "w")


    @patch("cli2.glob.glob")  
    @patch("cli2.storage.Client")  
    @patch("cli2.os.path.join", side_effect=lambda *args: "/".join(args))  
    def test_upload(self, mock_path_join, mock_storage_client, mock_glob):
        "Tests functionality of upload function"
        mock_glob.side_effect = [
            ["file1.json", "file2.json"], 
            ["file1.csv", "spotify_playlist_data.csv"],  
            ["file1.txt"],  
        ]
        
        expected_files = ["file1.json", "file2.json", "file1.csv", "file1.txt"]

        # Mock storage client and bucket
        mock_bucket = MagicMock()
        mock_storage_client_instance = mock_storage_client.return_value
        mock_storage_client_instance.bucket.return_value = mock_bucket
        
        # Mock bucket.blob to get a mock blob object
        mock_blob = MagicMock()
        mock_bucket.blob.return_value = mock_blob

        version = "v1.0"
        upload(version)

        # Verify that glob was called to retrieve files
        mock_glob.assert_has_calls([call("*.jsonl"), call("*.csv"), call("*.txt")], any_order=True)


if __name__ == "__main__":
    unittest.main()
