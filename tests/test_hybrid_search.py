
import unittest
from unittest.mock import patch

from src.retrieval.hybrid_search import hybrid_search


class TestHybridSearch(unittest.TestCase):

    @patch("src.retrieval.hybrid_search.search_papers")
    @patch("src.retrieval.hybrid_search.keyword_search")
    def test_combines_search_results(self, mock_keyword, mock_semantic):
        mock_semantic.return_value = [
            {
                "arxiv_id": "2401.00001",
                "title": "Example paper",
                "similarity": 0.9,
            }
        ]
        mock_keyword.return_value = [
            {
                "arxiv_id": "2401.00001",
                "title": "Example paper",
                "similarity": 0.8,
            }
        ]

        results = hybrid_search("example research", limit=5)

        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]["arxiv_id"], "2401.00001")


if __name__ == "__main__":
    unittest.main()
