
import unittest

from src.retrieval.semantic_search import keyword_search


class TestKeywordSearch(unittest.TestCase):

    def test_finds_paper_with_matching_terms(self):
        results = keyword_search("robot self-improving robots")

        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]["arxiv_id"], "2610.12424")

    def test_empty_query_raises_error(self):
        with self.assertRaises(ValueError):
            keyword_search("   ")


if __name__ == "__main__":
    unittest.main()
