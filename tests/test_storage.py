
import tempfile
import unittest
from pathlib import Path

from src.ingestion.fetch_papers import parse_feed
from src.ingestion.storage import load_papers, save_papers

from tests.test_fetch_papers import SAMPLE_XML


class TestStorage(unittest.TestCase):

    def test_save_and_load_papers(self):
        original = parse_feed(SAMPLE_XML)

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "papers.json"

            save_papers(original, path)
            loaded = load_papers(path)

        self.assertEqual(loaded, original)
        self.assertEqual(loaded[0].arxiv_id, "2401.00001")
        self.assertEqual(loaded[0].version, 2)


if __name__ == "__main__":
    unittest.main()
