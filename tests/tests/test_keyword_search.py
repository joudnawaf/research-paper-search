
import unittest
from unittest.mock import patch

from src.retrieval.semantic_search import keyword_search


class TestKeywordSearch(unittest.TestCase):

    @patch("src.retrieval.semantic_search.psycopg.connect")
    def test_finds_paper_with_matching_terms(self, mock_connect):
        mock_conn = mock_connect.return_value.__enter__.return_value
        mock_cur = mock_conn.cursor.return_value.__enter__.return_value
        mock_cur.fetchall.return_value = [
            (
                "2610.12424",
                "Robot self-improvement",
                0,
                "Research about self-improving robots",
                0.5,
            )
        ]

        results = keyword_search("robot self-improving robots")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["arxiv_id"], "2610.12424")
        self.assertGreater(results[0]["similarity"], 0)

    def test_empty_query_raises_error(self):
        with self.assertRaises(ValueError):
            keyword_search("   ")


if __name__ == "__main__":
    unittest.main()
