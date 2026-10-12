
import unittest
from unittest.mock import patch

import ollama


class TestOllama(unittest.TestCase):

    @patch("ollama.chat")
    def test_chat_returns_response(self, mock_chat):
        mock_chat.return_value = {
            "message": {
                "role": "assistant",
                "content": "RAG combines retrieval with generation."
            }
        }

        response = ollama.chat(
            model="qwen2.5:3b",
            messages=[
                {
                    "role": "user",
                    "content": "Explain RAG in one simple sentence."
                }
            ],
        )

        self.assertIn("RAG", response["message"]["content"])
        mock_chat.assert_called_once()


if __name__ == "__main__":
    unittest.main()
