
import unittest

from src.retrieval.semantic_search import search_papers


class TestSemanticSearch(unittest.TestCase):

    def test_finds_stored_paper(self):
        results = search_papers("testing research paper parsing")

        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]["arxiv_id"], "2401.00001")
        self.assertGreater(results[0]["similarity"], 0)


if __name__ == "__main__":
    unittest.main()
