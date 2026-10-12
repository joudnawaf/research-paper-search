
import unittest
from unittest.mock import patch

from src.retrieval.semantic_search import search_papers


class TestSemanticSearch(unittest.TestCase):

    @patch("src.retrieval.semantic_search.generate_embeddings")
    @patch("src.retrieval.semantic_search.psycopg.connect")
    def test_finds_stored_paper(self, mock_connect, mock_embeddings):
        mock_embeddings.return_value = [[0.1] * 384]

        mock_conn = mock_connect.return_value.__enter__.return_value
        mock_cur = mock_conn.cursor.return_value.__enter__.return_value
        mock_cur.fetchall.return_value = [
            ("2401.00001", "Example research paper", 0, "Example text", 0.85)
        ]

        results = search_papers("testing research paper parsing")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["arxiv_id"], "2401.00001")
        self.assertGreater(results[0]["similarity"], 0)

    def test_empty_query_raises_error(self):
        with self.assertRaises(ValueError):
            search_papers("   ")


if __name__ == "__main__":
    unittest.main()
